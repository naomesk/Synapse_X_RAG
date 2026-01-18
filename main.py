from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(
    title="LLM Gateway API",
    version="1.0",
    description="AI Assistant Backend for Capstone Project"
)

class QueryRequest(BaseModel):
    user_id: str
    user_role: str
    query: str
    debug: bool = False

class QueryResponse(BaseModel):
    answer: str
    execution_time: float
    intent: str
    source: str

@app.get("/")
def root():
    return {"message": "LLM Gateway API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/assistant/query")
def process_query(request: QueryRequest):
    start_time = time.time()
    
    query_lower = request.query.lower()
    
    # Intent classification
    if any(word in query_lower for word in ["select", "from", "where", "sql"]):
        intent = "sql_query"
        answer = f"SQL Query Analysis: '{request.query}'. Recommendation: Add proper indexing."
        source = "sql_analyzer"
    elif any(word in query_lower for word in ["compare", "similar", "find like", "vector"]):
        intent = "vector_search"
        answer = f"Vector Search Results: Found 5 relevant documents for: '{request.query}'"
        source = "vector_db"
    else:
        intent = "general_ai"
        answer = f"AI Response to: '{request.query}'. This is a simulated LLM response."
        source = "llm_service"
    
    execution_time = round(time.time() - start_time, 3)
    
    response = QueryResponse(
        answer=answer,
        execution_time=execution_time,
        intent=intent,
        source=source
    )
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)