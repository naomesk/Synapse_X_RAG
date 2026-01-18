from typing import Tuple

def process_llm_request(query: str, intent: str, user_role: str, debug=False) -> Tuple[str, str]:
    """Process query through LLM with security awareness"""
    
    # Check for sensitive data
    sensitive_keywords = ["internal", "confidential", "secret", "password", "ssn", "credit card"]
    
    if any(word in query.lower() for word in sensitive_keywords):
        if user_role != "admin":
            return "Access denied: Query contains sensitive information.", "BLOCKED"
        return call_local_llm(query, intent)  # Only for admins
    
    # Routing based on query type
    if intent == "SQL_QUERY":
        return call_sql_analyzer(query)
    elif intent == "VECTOR_QUERY":
        return call_vector_search(query)
    else:
        return call_general_llm(query)

def call_local_llm(query: str, intent: str) -> Tuple[str, str]:
    """Call local LLM (placeholder)"""
    answer = f"[LOCAL LLM - SAFE MODE]\nQuery: {query}\nIntent: {intent}"
    source = "Local Knowledge Base"
    return answer, source

def call_sql_analyzer(query: str) -> Tuple[str, str]:
    """Process SQL queries (placeholder)"""
    answer = f"[SQL ANALYZER]\nAnalyzed query: {query}\nSuggested optimization: Add indexes"
    source = "SQL Schema Repository"
    return answer, source

def call_vector_search(query: str) -> Tuple[str, str]:
    """Vector search (placeholder)"""
    answer = f"[VECTOR SEARCH]\nFound similar documents for: {query}"
    source = "Vector Database"
    return answer, source

def call_general_llm(query: str) -> Tuple[str, str]:
    """General LLM (placeholder)"""
    answer = f"[GENERAL LLM]\nAnswer to: {query}\nThis is a simulated response for demonstration."
    source = "External Knowledge Base"
    return answer, source

def call_openai_llm(query: str, intent: str) -> Tuple[str, str]:
    """External LLM (placeholder)"""
    answer = f"[CLOUD LLM RESPONSE] Answer for: {query}"
    source = "External Knowledge Base"
    return answer, source