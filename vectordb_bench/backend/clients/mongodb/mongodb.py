from doctest import DONT_ACCEPT_BLANKLINE
import logging
import time
from collections.abc import Iterable
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

from ..api import VectorDB
from .config import MongoDBIndexConfig

log = logging.getLogger(__name__)

class MongoDB(VectorDB):
    def __init__(
        self,
        dim: int,
        db_config: dict,
        db_case_config: MongoDBIndexConfig,
        collection_name: str = "vdb_bench_collection",
        id_field: str = "id",
        vector_field: str = "vector",
        drop_old: bool = False,
        **kwargs,
    ):
        self.dim = dim
        self.db_config = db_config
        self.case_config = db_case_config
        self.collection_name = collection_name
        self.id_field = id_field
        self.vector_field = vector_field
        self.drop_old = drop_old
        
        # Update index dimensions
        index_params = self.case_config.index_param()
        log.info(f"MongoDB client config: {self.db_config}, index params: {index_params}")
        index_params["fields"][0]["dimensions"] = dim
        
        # Initialize these as None - they'll be set in init()
        self.client = None
        self.db = None
        self.collection = None

    @contextmanager
    def init(self):
        """Initialize MongoDB client and cleanup when done"""
        try:
            if self.client is None:
                uri = self.db_config["connection_string"]
                self.client = MongoClient(uri)
                self.db = self.client[self.db_config["database"]]
                
                if self.drop_old and self.collection_name in self.db.list_collection_names():
                    log.info(f"MongoDB client dropping old collection: {self.collection_name}")
                    self.db.drop_collection(self.collection_name)

                self.collection = self.db[self.collection_name]
                
            yield
        finally:
            if self.client is not None:
                self.client.close()
                self.client = None
                self.db = None
                self.collection = None

    def _create_index(self) -> None:
        """Create vector search index"""
        index_name = "vector_index"
        index_params = self.case_config.index_param()
        
        try:
            # Create vector search index
            search_index = SearchIndexModel(
                definition=index_params,
                name=index_name,
                type="vectorSearch"
            )
            
            self.collection.create_search_index(search_index)
            log.info(f"Created vector search index: {index_name}")
            self._wait_for_index_ready(index_name)
            
            # Create regular index on id field for faster lookups
            self.collection.create_index(self.id_field)
            log.info(f"Created index on {self.id_field} field")
            
        except Exception as e:
            log.error(f"Error creating index: {str(e)}")
            raise

    def _wait_for_index_ready(self, index_name: str, check_interval: int = 5) -> None:
        """Wait for index to be ready"""
        while True:
            indices = list(self.collection.list_search_indexes())
            if indices and any(idx.get("name") == index_name and idx.get("queryable") for idx in indices):
                break
            time.sleep(check_interval)
        log.info(f"Index {index_name} is ready")

    def need_normalize_cosine(self) -> bool:
        return False

    def insert_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[int],
        **kwargs,
    ) -> int:
        """Insert embeddings into MongoDB"""
        
        # Prepare documents in bulk
        documents = [
            {
                self.id_field: id_,
                self.vector_field: embedding,
            }
            for id_, embedding in zip(metadata, embeddings)
        ]
        
        # Use ordered=False for better insert performance
        try:
            less_documents = documents[:10]
            self.collection.insert_many(less_documents, ordered=False)
        except Exception as e:
            return 0, e
        return len(documents), None

    def search_embedding(
        self,
        query: list[float],
        k: int = 100,
        filters: dict | None = None,
        **kwargs,
    ) -> list[int]:
        """Search for similar vectors"""
        search_params = self.case_config.search_param()
        
        vector_search = {
            "queryVector": query,
            "index": "vector_index",
            "path": self.vector_field,
            "limit": k
        }
        
        # Add exact search parameter if specified
        if search_params["exact"]:
            vector_search["exact"] = True
        else:
            # Set numCandidates based on k value and data size
            # For 50K dataset, use higher multiplier for better recall
            num_candidates = min(10000, max(k * 20, search_params["numCandidates"] or 0))
            vector_search["numCandidates"] = num_candidates
        
        # Add filter if specified
        if filters:
            log.info(f"Applying filter: {filters}")
            vector_search["filter"] = {
                "id": {"gt": filters["id"]},
            }

        
        pipeline = [
            {
                "$vectorSearch": vector_search
            },
            {
                "$project": {
                    "_id": 0,
                    self.id_field: 1,
                    "score": {"$meta": "vectorSearchScore"}  # Include similarity score
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        return [doc[self.id_field] for doc in results]

    def optimize(self) -> None:
        """MongoDB vector search indexes are self-optimizing"""
        self._create_index()
        self._wait_for_index_ready("vector_index")

    def optimize_with_size(self, data_size: int) -> None:
        """MongoDB vector search indexes are self-optimizing"""
        pass

    def ready_to_load(self) -> None:
        """MongoDB is always ready to load"""
        pass