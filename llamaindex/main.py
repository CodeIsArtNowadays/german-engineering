import chromadb

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PyMuPDFReader

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
# Load documents
extractor = {'.pdf': PyMuPDFReader()}
documents = SimpleDirectoryReader('data', file_extractor=extractor).load_data() # pyright: ignore

# DB settins
chroma_client = chromadb.PersistentClient(path='./vector_db')
chroma_collection = chroma_client.get_or_create_collection(name='ragged')
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Add documents to context
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

# Quering

def query_handler(query: str):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)

def retrieve_and_synth_by_hand(query: str):
    retriever = index.as_retriever(similarity_top_k=2)
    nodes = retriever.retrieve(query)

    for n in nodes:
        print(f'{n.text}\n{n.score}\n')

    from llama_index.core.response_synthesizers import get_response_synthesizer
    synthesizer = get_response_synthesizer()
    response = synthesizer.synthesize(query, nodes=nodes)
    print(response)

query = "Who is the current CFO of BrightPath Solutions?"

retrieve_and_synth_by_hand(query)

