from fastapi import FastAPI
from pydantic import BaseModel
from search import RAGSystem   # import your RAG system

app = FastAPI()

# Initialize RAG system once at startup
rag = RAGSystem(data_path="recipes.json")

class ChatQuery(BaseModel):
    query: str

@app.get("/recipes/search")
def search_recipes(q: str = ""):
    if not q:
        return rag.employees  # still holds recipes in self.employees
    results = [
        recipe for recipe in rag.employees
        if q.lower() in str(recipe).lower()
    ]
    return results

@app.post("/chat")
def chat_handler(chat_query: ChatQuery):
    response_text = rag.process_query(chat_query.query)
    return {"response": response_text}
