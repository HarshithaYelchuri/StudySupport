import streamlit as st
import os
from PIL import Image
from backend.pdf_loader import load_pdf_text
from backend.vector_store import create_vector_store, load_vector_store
from backend.qa_chain import ask_question
from backend.quiz_generator import generate_mcq_quiz, parse_mcq_output
from reportlab.pdfgen import canvas

DB_PATH = "data/db"
UPLOAD_FOLDER = "data/uploads"
#logo SS
LOGO_PATH = "data/logo.png"
def show_header():
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(logo, width=70)
        with col2:
            st.markdown(
                """
                <h1 style='padding-top: 15px; font-size: 40px;'>StudySupport</h1>
                """,
                unsafe_allow_html=True
            )
    else:
        st.title("StudySupport")

show_header()

if "page" not in st.session_state:
    st.session_state.page = "upload"
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = {}

# Pages
def show_page():
    if st.session_state.page == "upload":
        show_upload_page()
    elif st.session_state.page == "ask":
        show_ask_page()
    elif st.session_state.page == "quiz":
        show_quiz_page()

# Upload Page
def show_upload_page():
    st.subheader("📤 Upload your PDF")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.pdf_path = file_path

        raw_text = load_pdf_text(file_path)
        create_vector_store(raw_text, DB_PATH)
        st.success("✅ PDF processed successfully!")

        st.write("### What do you want to do?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💬 Ask a Question"):
                st.session_state.page = "ask"
                st.rerun()

        with col2:
            if st.button("📝 Generate Quiz"):
                st.session_state.page = "quiz"
                st.rerun()

# Ask question Page
def show_ask_page():
    st.subheader("💬 Ask your PDF")

    question = st.chat_input("Type your question here")

    if question:
        db = load_vector_store(DB_PATH)
        docs = db.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        answer = ask_question(context, question)

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(answer)

    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "upload"
            st.rerun()

    with col2:
        if st.button("📝 Generate Quiz"):
            st.session_state.page = "quiz"
            st.rerun()

# Quiz Page
def show_quiz_page():
    st.subheader("📝 Generate a Quiz")

    difficulty_map = {"Easy": "basic", "Medium": "advanced", "Challenging": "hard"}
    ui_difficulty = st.selectbox("📊Select Difficulty", list(difficulty_map.keys()))
    difficulty = difficulty_map[ui_difficulty]

    num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5, step=1)

    if st.button("Generate Quiz"):
        db = load_vector_store(DB_PATH)
        docs = db.similarity_search("generate quiz", k=5)
        context = "\n\n".join([doc.page_content for doc in docs])

        quiz_text = generate_mcq_quiz(context, difficulty=difficulty, num_questions=num_questions)
        st.session_state.quiz_state = {
            "questions": parse_mcq_output(quiz_text),
            "submitted": [False] * num_questions,
            "feedback": [""] * num_questions,
            "score": 0
        }
        st.rerun()

    if "questions" in st.session_state.quiz_state:
        render_quiz()

    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "upload"
            st.session_state.quiz_state = {}
            st.rerun()

    with col2:
        if st.button("💬 Ask a Question"):
            st.session_state.page = "ask"
            st.rerun()

def render_quiz():
    quiz_state = st.session_state.quiz_state

    st.markdown("### 🎯 Quiz")

    for idx, q in enumerate(quiz_state["questions"]):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")

        options_list = list(q["options"].items())
        selected = st.radio(
            "Options:",
            options_list,
            format_func=lambda x: f"{x[0]}. {x[1]}",
            index=None,
            key=f"radio_{idx}"
        )

        if not quiz_state["submitted"][idx]:
            if st.button("Submit", key=f"submit_{idx}"):
                quiz_state["submitted"][idx] = True
                if selected and selected[0] == q["answer"]:
                    quiz_state["score"] += 1
                    quiz_state["feedback"][idx] = f"✅ Correct! {q['explanation']}"
                else:
                    quiz_state["feedback"][idx] = f"❌ Incorrect. Correct answer: {q['answer']}. {q['explanation']}"
                st.rerun()

        if quiz_state["submitted"][idx]:
            if "✅" in quiz_state["feedback"][idx]:
                st.success(quiz_state["feedback"][idx])
            else:
                st.error(quiz_state["feedback"][idx])

        st.write("---")

    if all(quiz_state["submitted"]):
        st.markdown(f"### Final Score: `{quiz_state['score']}/{len(quiz_state['questions'])}`")

        if st.button("📥 Export Quiz to PDF"):
            export_quiz_to_pdf()

# Export Quiz to PDF
def export_quiz_to_pdf():
    quiz_state = st.session_state.quiz_state
    export_path = "data/quiz_output.pdf"
    c = canvas.Canvas(export_path)
    c.setFont("Helvetica", 12)
    y = 800

    if os.path.exists(LOGO_PATH):
        c.drawInlineImage(LOGO_PATH, 40, y, width=100, preserveAspectRatio=True)
        y -= 100

    for idx, q in enumerate(quiz_state["questions"]):
        c.drawString(40, y, f"Q{idx + 1}: {q['question']}")
        y -= 20
        for opt_key, opt_val in q["options"].items():
            c.drawString(60, y, f"{opt_key}. {opt_val}")
            y -= 20
        feedback = quiz_state["feedback"][idx].replace("✅ ", "").replace("❌ ", "")
        c.drawString(60, y, feedback)
        y -= 40
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800

    c.save()
    with open(export_path, "rb") as f:
        st.download_button("⬇️ Download Quiz PDF", f, file_name="quiz.pdf")

# Run App
show_page()
