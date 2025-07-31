import os
import streamlit as st
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondenseQuestionChatEngine


DOCS_PATH = "E:/rag_app/guidline-docs"
STORAGE_PATH = "E:/rag_app/vectorstore"

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en",
    embed_batch_size=8,
    device="cpu"
)
Settings.llm = Ollama(model="mistral", request_timeout=300.0)

@st.cache_resource
def load_or_build_index():
    if os.path.exists(STORAGE_PATH):
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_PATH)
        return load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader(DOCS_PATH).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=STORAGE_PATH)
        return index

def setup_chat_engine(index):
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    query_engine = index.as_query_engine(similarity_top_k=3)
    return CondenseQuestionChatEngine.from_defaults(
        llm=Settings.llm,
        memory=memory,
        query_engine=query_engine
    )

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.chat_engine = setup_chat_engine(load_or_build_index())

st.set_page_config(page_title="Guideline RAG Chatbot", layout="centered")
st.title("Company Guidelines Chatbot")
st.caption("Ask questions about your coding guidelines (PHP, MERN, HTML/CSS/JS).")

if st.button("Clear Chat", help="Click to clear all messages"):
    clear_chat()
    st.experimental_rerun()

index = load_or_build_index()

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = setup_chat_engine(index)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

user_input = st.chat_input("Ask your question here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.status("Thinking...", expanded=False) as status:
        try:
            response = st.session_state.chat_engine.chat(user_input)
            st.session_state.chat_history.append(("assistant", response.response))

            status.update(label="Response ready!", state="complete")
        except Exception as e:
            error_message = f"An error occurred: {e}"
            st.session_state.chat_history.append(("assistant", error_message))
            status.update(label="Error!", state="error")
    
    with st.chat_message("assistant"):
        st.markdown(response.response if 'response' in locals() else error_message)