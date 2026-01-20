class Database:
    def _chunk_document(self, content: str) -> list[dict]:
        """
        Splits document content into chunks.
        Returns list of dicts with keys: chunk_id, content, position
        """
        pass
    
    def _embed_chunks(self, chunks: list[dict]) -> list[tuple[int, list[float]]]:
        """
        Embeds list of chunk dicts.
        Returns list of tuples: (chunk_id, embedding_vector)
        """
        pass

    def add_document(self, document_id: str, content: str, metadata: dict):
        """
        Atomically:
        - chunks document
        - inserts chunk rows into SQLite
        - embeds chunks
        - inserts vectors into Milvus
        Guarantees no partial ingestion.
        """
        pass

    def delete_document(self, document_id: str):
        """
        Removes document from SQLite and Milvus.
        """
        pass
    def query(self, query_embedding: list[float], top_k: int = 5, filters: dict | None = None):
        """
        - Vector search in Milvus
        - Metadata join via SQLite
        - Returns ordered chunk payloads
        """
        pass

    def get_chunk(self, chunk_id: int)-> dict:
        """
        Retrieves a chunk by its ID.
        """
        pass

    def check_alignment(self)-> dict:
        """
        Compares entries in SQLite and Milvus to find discrepancies.
        """
        pass

    def repair_alignment(self)-> None:
        """
        Re-embeds missing chunks and removes orphaned vectors.
        """
        pass

