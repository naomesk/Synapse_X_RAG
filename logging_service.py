import logging
from datetime import datetime

def init_logger():
    """Initialize application logger"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )

def log_query(user_id: str, query: str, intent: str, duration: float):
    """Log query details"""
    logger = logging.getLogger(__name__)
    logger.info(f"Query | User: {user_id} | Intent: {intent} | Duration: {duration}s | Query: {query[:50]}...")