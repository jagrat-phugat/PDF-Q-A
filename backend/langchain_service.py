import os
from dotenv import load_dotenv
import google.generativeai as genai
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found")
genai.configure(api_key=api_key)

# Use only the free Gemini model
model = genai.GenerativeModel("models/gemini-pro")

# Setup embedding model once globally
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

async def get_answer(text: str, question: str) -> str:
    document = Document(text=text)
    index = VectorStoreIndex.from_documents([document])
    retriever = index.as_retriever(similarity_top_k=2)
    relevant_nodes = retriever.retrieve(question)
    context = "\n\n".join([node.text for node in relevant_nodes])[:1000]

    prompt = f"""
Answer the following question using only the provided context.
If the context is not sufficient, respond with "I don't know."

Context:
{context}

Question:
{question}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
