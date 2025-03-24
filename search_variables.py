import json
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="census_variables_1",
    embedding_function=embeddings,
    persist_directory="./chroma_census_db/census_variables_1",  # Where to save data locally, remove if not necessary
)

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

for i in range(len(census_data)):
    item = census_data[i]
    category = item['category']
    print('Checking dataset', category)

    results = vector_store.similarity_search(
        "the",
        filter={"category": category}
    )

    print(len(results))
    if (len(results) == 0):
        break
# for res in results:
#     print(res.metadata['category'])