from query_controller import QueryRequest

def validate_request(request: QueryRequest) -> bool:
    """Validate request correctness"""
    if not request.user_id or not request.user_role or not request.query:
        return False
    if len(request.query.strip()) < 1:
        return False
    return True

def classify_intent(query: str) -> str:
    """Classify query intent"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["select", "insert", "update", "delete", "from", "where"]):
        return "SQL_QUERY"
    
    if any(word in query_lower for word in ["compare", "similar", "find like", "vector"]):
        return "VECTOR_QUERY"
    
    if any(word in query_lower for word in ["summarize", "explain", "describe"]):
        return "ANALYTICAL_QUERY"
    
    return "GENERAL_QUERY"

def authorize_request(user_role: str) -> bool:
    """Check access permissions"""
    allowed_roles = ["user", "admin", "analyst"]
    return user_role.lower() in allowed_roles