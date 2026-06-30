import chromadb


class LongTermMemory:
    """
    Stores and retrieves research summaries using ChromaDB.
    """

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="research_memory"
        )

    def add(self, query: str, report: str):
        doc_id = str(abs(hash(query + report)))

        self.collection.add(
            documents=[report],
            metadatas=[{"query": query}],
            ids=[doc_id],
        )

    def search(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        return results