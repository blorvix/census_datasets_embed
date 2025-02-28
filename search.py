from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="census_datasets",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db/short",  # Where to save data locally, remove if not necessary
)

results = vector_store.similarity_search(
    "How many businesses in the United States are owned by people of different racial groups in 2019?",
    # "How many people are unemployed in August, 1989?",
    k=10,
)
for res in results:
    print(res.metadata['category'])