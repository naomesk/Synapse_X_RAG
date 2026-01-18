from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter()

# Request/Response Models
class QueryRequest(BaseModel):
    user_id: str
    user_role: str
    query: str
    debug: Optional[bool] = False

class QueryResponse(BaseModel):
    answer: str
    execution_time: float
    intent: str
    source: Optional[str] = None
    debug_info: Optional[dict] = None

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query through AI pipeline"""
    
    start_time = time.time()
    
    try:
        # 1. Basic validation
        if not request.query or len(request.query.strip()) < 2:
            raise HTTPException(status_code=400, detail="Query is too short")
        
        # 2. Determine intent
        intent = "general"
        query_lower = request.query.lower()
        
        if any(word in query_lower for word in ["select", "from", "where", "sql"]):
            intent = "sql_query"
        elif any(word in query_lower for word in ["compare", "similar", "find like"]):
            intent = "vector_search"
        
        # 3. Process based on intent (simulated)
        if intent == "sql_query":
            answer = f"SQL analysis for: {request.query}"
            source = "database_schema"
        elif intent == "vector_search":
            answer = f"Vector search results for: {request.query}"
            source = "vector_database"
        else:
            answer = f"AI response to: {request.query}"
            source = "knowledge_base"
        
        execution_time = round(time.time() - start_time, 3)
        
        # 4. Prepare response
        response = QueryResponse(
            answer=answer,
            execution_time=execution_time,
            intent=intent,
            source=source
        )
        
        if request.debug:
            response.debug_info = {
                "user_role": request.user_role,
                "query_length": len(request.query),
                "timestamp": start_time
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))