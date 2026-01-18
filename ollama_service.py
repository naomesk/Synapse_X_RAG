import ollama
import logging
from typing import Dict, Tuple
import time

logger = logging.getLogger(__name__)

class OllamaService:
    """Core Ollama LLM service for AI responses"""
    
    def __init__(self):
        self.default_model = "llama2"
        self.model_cache = {}
        self._init_service()
    
    def _init_service(self):
        """Initialize and check Ollama availability"""
        try:
            models = ollama.list()
            self.available_models = [m['name'] for m in models.get('models', [])]
            
            if not self.available_models:
                logger.warning("No Ollama models found. Please run: ollama pull llama2")
                self.available_models = [self.default_model]
            
            logger.info(f"Ollama initialized. Models: {self.available_models}")
            
        except Exception as e:
            logger.error(f"Ollama initialization failed: {e}")
            self.available_models = []
    
    def is_available(self) -> bool:
        """Check if Ollama is ready to use"""
        return len(self.available_models) > 0
    
    def generate_response(self, query: str, intent: str = "GENERAL", context: str = None) -> Tuple[str, Dict]:
        """
        Generate AI response using Ollama
        
        Returns:
            Tuple of (response_text, metadata)
        """
        start_time = time.time()
        
        if not self.is_available():
            return self._get_fallback_response(query, intent), {
                "source": "mock",
                "model": "none",
                "error": "Ollama not available"
            }
        
        try:
            model = self._select_model(intent)
            prompt = self._build_prompt(query, intent, context)
            
            logger.info(f"Calling Ollama | Model: {model} | Intent: {intent}")
            
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(intent)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.7,
                    "num_predict": 512
                }
            )
            
            response_time = time.time() - start_time
            
            metadata = {
                "source": "ollama",
                "model": model,
                "response_time": round(response_time, 3),
                "tokens": len(response['message']['content'].split()),
                "intent": intent
            }
            
            logger.info(f"Ollama response received in {response_time:.2f}s")
            
            return response['message']['content'], metadata
            
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return self._get_fallback_response(query, intent), {
                "source": "error",
                "model": "none",
                "error": str(e)
            }
    
    def _select_model(self, intent: str) -> str:
        """Select appropriate model for the intent"""
        model_mapping = {
            "SQL_QUERY": "codellama",
            "CODE_QUERY": "codellama",
            "ANALYTICAL_QUERY": "llama2",
            "VECTOR_QUERY": "llama2",
            "GENERAL_QUERY": "llama2"
        }
        
        preferred = model_mapping.get(intent, self.default_model)
        
        if preferred in self.available_models:
            return preferred
        elif self.available_models:
            return self.available_models[0]
        else:
            return self.default_model
    
    def _get_system_prompt(self, intent: str) -> str:
        """Get system prompt based on intent"""
        prompts = {
            "SQL_QUERY": "You are an expert SQL database administrator. Analyze queries and provide optimization suggestions.",
            "CODE_QUERY": "You are an expert software developer. Help with code analysis and programming questions.",
            "ANALYTICAL_QUERY": "You are a data analyst. Help explain concepts and analyze information.",
            "VECTOR_QUERY": "You assist with document search and information retrieval systems.",
            "GENERAL_QUERY": "You are a helpful AI assistant. Provide clear, accurate answers."
        }
        return prompts.get(intent, "You are a helpful AI assistant.")
    
    def _build_prompt(self, query: str, intent: str, context: str = None) -> str:
        """Build user prompt with context"""
        if intent == "SQL_QUERY":
            base = f"Analyze this SQL query:\n\n```sql\n{query}\n```\n\n"
            base += "Provide:\n1. What the query does\n2. Potential performance issues\n3. Optimization suggestions\n4. Index recommendations if applicable"
        
        elif intent == "VECTOR_QUERY":
            base = f"Document search query:\n\n'{query}'\n\n"
            base += "Suggest:\n1. Better search terms\n2. Relevant document types\n3. Search strategy improvements"
        
        elif intent == "ANALYTICAL_QUERY":
            base = f"Please explain:\n\n{query}\n\n"
            base += "Provide a clear, structured explanation."
        
        else:
            base = query
        
        if context:
            base = f"Context: {context}\n\nQuestion: {base}"
        
        return base
    
    def _get_fallback_response(self, query: str, intent: str) -> str:
        """Fallback response when Ollama is unavailable"""
        fallbacks = {
            "SQL_QUERY": f"SQL Analysis:\nQuery: {query}\n\n(Ollama would analyze this SQL query for optimization opportunities)",
            "VECTOR_QUERY": f"Document Search:\nLooking for: '{query}'\n\n(Ollama would help refine search terms and strategy)",
            "ANALYTICAL_QUERY": f"Analysis:\nTopic: {query}\n\n(Ollama would provide detailed explanation and analysis)",
            "GENERAL_QUERY": f"AI Response:\nQuestion: {query}\n\n(Ollama would provide an intelligent answer to this question)"
        }
        return fallbacks.get(intent, f"Response to: {query}")

# Global instance
ollama = OllamaService()