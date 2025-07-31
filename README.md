# Company Guidelines RAG Chatbot

This is a **locally running, free, and private chatbot** built using `LlamaIndex`, `Streamlit`, and `Ollama`. It allows you to ask questions about your internal coding guideline documents (e.g., PHP, MERN, HTML/CSS/JS) — without using any paid APIs like OpenAI.

> This system uses **RAG (Retrieval-Augmented Generation)** powered by local embeddings and local LLMs — fully offline and CPU-compatible.

---

## Folder Setup

Create a folder named `guidline-docs` anywhere on your system, for example:

/Users/yourname/projects/guidline-docs/

javascript
Copy
Edit

Put your `.txt` guideline files inside this folder:

guidline-docs/
├── php.txt
├── mern.txt
└── html-css-js.txt

java
Copy
Edit

Now update the folder path in your `app.py` like this:

```python
DOCS_PATH = "YOUR/DIRECTORY/PATH/guidline-docs"
STORAGE_PATH = "YOUR/DIRECTORY/PATH/vectorstore"
How to Run Locally
1. Install Requirements
Make sure Python 3.9+ is installed.

bash
Copy
Edit
pip install -r requirements.txt
2. Run Ollama and Download Model
Make sure Ollama is installed and running:

bash
Copy
Edit
ollama run mistral
You can also use lighter models like tinyllama, llama2, or gemma.

3. Run Streamlit App
bash
Copy
Edit
streamlit run app.py
Features
    Load multiple .txt documents as knowledge base

    Ask questions in natural language

    Fully offline — uses Ollama models like mistral

    Local CPU-based embeddings (e.g. BAAI/BGE or MiniLM)

    Chat memory — follow-up questions are understood

    "Clear Chat" resets history without reloading documents

    How to Add Your Own Guidelines
Go to the folder you set as DOCS_PATH

Add .txt files like:

security.txt

frontend-standards.txt

docker-best-practices.txt

Restart the app. All files will be automatically indexed and you can start chatting about them.

    Notes
App currently supports only .txt files inside your guidline-docs folder.

Embeddings are stored and reused in the vectorstore folder to avoid reprocessing on each run.

Performance may be slow on low-end CPUs. For better speed, use lightweight models like:

bash
Copy
Edit
ollama run tinyllama