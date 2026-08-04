import chromadb

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PyMuPDFReader
from llama_index.vector_stores.chroma import ChromaVectorStore

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

# DB settins
chroma_client = chromadb.PersistentClient(path='./vector_db')
chroma_collection = chroma_client.get_or_create_collection(name='ragged')
print(chroma_collection.count())
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)


def query_handler(query: str, index):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)

def retrieve_and_synth_by_hand(query: str, index):
    retriever = index.as_retriever(similarity_top_k=2)
    nodes = retriever.retrieve(query)

    for n in nodes:
        print(f'{n.text}\n{n.score}\n')

    from llama_index.core.response_synthesizers import get_response_synthesizer
    synthesizer = get_response_synthesizer()
    response = synthesizer.synthesize(query, nodes=nodes)
    print(response)


def get_creating_index(path_to_documents_dir: str):
    # Load documents
    extractor = {'.pdf': PyMuPDFReader()}
    documents = SimpleDirectoryReader(path_to_documents_dir, file_extractor=extractor).load_data() # pyright: ignore
    # Creating context
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )
    # Add documents to context
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    storage_context.persist(persist_dir='./vector_db')
    return index

def get_retrieving_index():
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def main():
    # index = get_creating_index('data')
    index = get_retrieving_index()

    query = "When was BrightPath Solutions founded?"
    query_handler(query, index)

if __name__ == '__main__':
    main()