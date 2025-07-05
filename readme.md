
 🎓 StudySupport: AI-Powered PDF Q\&A + Quiz Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/Model-Gemini_1.5_Flash-yellow)](https://makersuite.google.com/app)

---

 📚 Table of Contents

* [Demo](#demo)
* [Overview](#overview)
* [Features](#features)
* [Installation](#installation)
* [How to Use](#how-to-use)
* [Directory Structure](#directory-structure)
* [Deployment](#deployment)
* [Future Scope](#future-scope)
* [Credits](#credits)
* [License](#license)

---

## 🚀 Demo

> 🔗 *Live App (Optional):* Coming soon...

### UI Preview:

![image](https://github.com/user-attachments/assets/4876c96a-7d58-4610-b2e1-428e8f70fed1)
![image](https://github.com/user-attachments/assets/ec62b4ff-ea99-45a0-961e-b20fa3878a30)
![image](https://github.com/user-attachments/assets/7b16d9d4-71b8-48b0-83f1-12efc41fa69b)
 




## 🧠 Overview

**StudySupport** is an interactive AI-powered tool designed for learners, educators, and content reviewers. Upload any **PDF** file and:

* Ask questions contextually about its content.
* Generate customized MCQ quizzes.
* Export the quiz as a professional **PDF**.

Built using **Streamlit**, **LangChain**, **FAISS**, and **Google's Gemini API**, the app delivers fast and meaningful interactions from any educational or reference material.

---

## 🔑 Features

* 📤 Upload and process any PDF
* 🤖 Ask contextual questions and get AI-generated answers
* 📝 Generate MCQ quizzes with difficulty & length control
* 📄 Export quizzes as beautifully formatted PDF
* 🔍 Semantic search via vector embeddings
* ⚡ Fast inference using **Gemini 1.5 Flash**

---

## ⚙️ Installation

> Requires **Python 3.11**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/studysupport.git
cd studysupport
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free API key from: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 💡 How to Use

Run the app with Streamlit:

```bash
streamlit run app.py
```

Then:

1. Upload your PDF document
2. Choose to either:

   * Ask questions about it
   * Generate a quiz
3. View and interact with results
4. Export quiz as PDF if needed

---

## 🗂 Directory Structure

```
studysupport/
├── app.py
├── .env
├── requirements.txt
├── backend/
│   ├── pdf_loader.py
│   ├── qa_chain.py
│   ├── quiz_generator.py
│   └── vector_store.py
├── data/
│   ├── uploads/
│   ├── db/                 # FAISS vector store
│   └── logo.png
├── screenshots/
│   ├── upload.png
│   ├── ask.png
│   └── quiz.png
├── LICENSE
└── README.md
```

---

## 🚀 Deployment

To deploy on **Streamlit Cloud**:

1. Push your code to a public GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **"New App"**, select your repo and `app.py`
4. Set `GEMINI_API_KEY` in *Advanced Settings → Secrets*
5. Click **Deploy**

---

## 🔮 Future Scope

* 📌 Topic tagging & categorization of PDFs
* 🗣️ Text-to-speech answers for better accessibility
* 🌐 Multi-language support
* 🧑‍🏫 Adaptive quizzes based on student performance
* 👥 User authentication and saved sessions

---

## 🙌 Credits

* [Google Generative AI](https://ai.google/discover/generativeai/)
* [LangChain](https://www.langchain.com/)
* [Streamlit](https://streamlit.io/)
* [FAISS by Facebook AI](https://github.com/facebookresearch/faiss)
* [ReportLab](https://www.reportlab.com/opensource/)

---

## 📄 License

Distributed under the **MIT License**.
See [`LICENSE`](LICENSE) for more details.

