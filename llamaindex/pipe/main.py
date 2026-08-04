import chromadb

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.ingestion.cache import SimpleCache
from llama_index.core.node_parser import SentenceSplitter 

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Settings
Settings.llm = Ollama(
    base_url='http://localhost:11434',
    model='llama3.2:3b',
    request_timeout=300,
    context_window=4096
)
Settings.embed_model = OllamaEmbedding(
    base_url='http://localhost:11434',
    model_name='all-minilm:33m',
    request_timeout=300,
)

chroma_client = chromadb.PersistentClient(path='./vector_db')
chroma_collection = chroma_client.get_or_create_collection(name='ragged')
print(chroma_collection.count())
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
documents = SimpleDirectoryReader('data').load_data()

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1024, chunk_overlap=20),
        Settings.embed_model
    ],
    vector_store=vector_store,
    docstore=SimpleDocumentStore(),
    cache=IngestionCache(cache=SimpleCache())
)

nodes = pipeline.run(documents=documents)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

querier = index.as_query_engine()
response = querier.query(' What color was the sailboat in the story?')

print(response)