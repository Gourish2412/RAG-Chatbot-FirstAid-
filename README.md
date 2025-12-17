# First Aid RAG Assistant (FAISS + FastAPI)

This project is a **Retrieval-Augmented Generation (RAG)** chatbot focused on **First Aid assistance**. It uses:

* **FAISS** for vector search
* **Sentence-Transformers** for embeddings
* **TinyLlama (Hugging Face)** for text generation
* **FastAPI** for the backend + simple web UI

The workflow is:

1. Build a FAISS index from text documents
2. Run a FastAPI server
3. Ask questions via browser or API

---

## 📁 Project Structure

```
.
├── app.py              # FastAPI app (RAG + UI)
├── build_index.py      # Script to build FAISS index
├── requirements.txt    # Python dependencies
├── docs/               # Your knowledge base (.txt files)
├── index_data/         # Generated FAISS index + metadata
│   ├── faiss.index
│   └── metadata.json
└── README.md
```

---

## ⚙️ Prerequisites

* Python **3.9 – 3.11** (recommended)
* Git (optional, for cloning)
* Internet connection (to download Hugging Face models)

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

⚠️ **Note:** `faiss-cpu` may take a few minutes to install.

---

## 📄 Add Your Knowledge Base

1. Create a folder named `docs/`
2. Add one or more `.txt` files inside it

Example:

```text
docs/first_aid.txt
docs/burns.txt
docs/cpr.txt
```

Each file should contain **plain text** (no PDFs).

---

## 🧠 Build the FAISS Index

Run the indexing script **once** (or whenever docs change):

```bash
python build_index.py
```

If successful, you will see:

```
index_data/
├── faiss.index
└── metadata.json
```

❌ If this step is skipped, the app will NOT start.

---

## ▶️ Run the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## 🌐 Access the App

* **Web UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **API Endpoint:** `POST /query`

Example API request:

```json
{
  "query": "What should I do for a burn?"
}
```

---

## 🩺 How It Works (High-Level)

1. User question is embedded using `all-MiniLM-L6-v2`
2. FAISS retrieves top relevant text chunks
3. Retrieved context is injected into the prompt
4. TinyLlama generates a grounded answer

If the answer is **not found in context**, the assistant advises seeking professional medical help.

---

## 🛠️ Common Issues & Fixes

### ❌ "Index files not found"

✔ Run:

```bash
python build_index.py
```

---

### ❌ Slow first response

✔ Models are loading for the first time (normal)

---

### ❌ Out of memory

✔ Use a smaller LLM or close other applications

---

## ⚠️ Medical Disclaimer

This project is for **educational purposes only**.
It does **NOT** replace professional medical advice.
Always consult a qualified healthcare provider in emergencies.

---

## 📜 License

MIT License (you can change this if needed)

---

## ⭐ Acknowledgements

* Hugging Face Transformers
* Sentence-Transformers
* FAISS by Meta
* FastAPI

---

