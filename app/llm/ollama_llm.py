from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings as LlamaSettings

from core.settings import Settings
import requests

def load_llm():
    llm = Ollama(
        model=Settings.OLLAMA_MODEL,
        request_timeout=600
    )
   

    embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


    LlamaSettings.llm = llm
    LlamaSettings.embed_model = embed_model

    return llm



def call_llm(prompt: str) -> str:
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": Settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    return res.json()["response"]

def call_llm_stream(prompt: str):
    llm = load_llm()
    for chunk in llm.stream_complete(prompt):
        yield chunk.delta
