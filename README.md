<<<<<<< HEAD
# med-assistant-chatbot
=======
# 🏥 Medical Assistant Chatbot

An AI-powered medical assistant that integrates **FastAPI**, **SQLAlchemy**, and **Streamlit**, allowing users to interact with patient records through a chatbot interface powered by **OpenAI GPT models**.

This project queries and summarizes data from a MySQL database — including patients, visits, tests, and more — using natural language.

---

## 📁 Project Structure

```
.
├── chat_ui.py          # Streamlit frontend
├── main.py             # FastAPI backend entry point
├── database.py         # Database configuration
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── routers/            # API routers
│   ├── patients.py
│   ├── visits.py
│   ├── tests.py
│   └── chat.py
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

Add your OpenAI API key to a `.env` file:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 🔐 Keep this file secret — do not commit it to Git.

---

### 3. Run FastAPI server

```bash
uvicorn main:app --reload
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 4. Run Streamlit UI

```bash
streamlit run chat_ui.py
```

Interface: [http://localhost:8501](http://localhost:8501)

---

## 💬 Example Prompts

- `"Get patient 3"`
- `"Visit 5"`
- `"Test 2"`
- `"Summarize visit 4"`
- `"Who prescribed test 7?"`

---

## 🧠 Features

- 🔍 Retrieve patient, visit, test, and prescription data
- 💬 Interact using natural language with GPT-3.5
- 🧩 Modular FastAPI architecture
- 🖥️ Easy-to-use chat interface via Streamlit
- 🔐 Secure key management with `.env`

---

## 📌 To Do

- Add login/authentication
- Add test coverage
- Improve error handling
- Optionally support other LLMs (DeepSeek, Together.ai)

---

