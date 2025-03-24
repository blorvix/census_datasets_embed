import json
import uuid

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

with open('data/census_choices.json', 'r') as file:
    choices = json.load(file)

# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
# vector_store = Chroma(
#     collection_name=f"census_choices",
#     embedding_function=embeddings,
#     persist_directory=f"./chroma_census_db/census_choices",
# )

documents = []

for variable, items in choices.items():
    for key, value in items.items():
        categories = value['categories']
        _value = value['value']
        metadata = {
            'variable': variable,
            'key': key,
        }
        for category in categories:
            metadata[category] = '1'

        print(f'Key: {key}\nValue: {_value}')
        print(metadata)
        
        # documents.append(Document(
        #     page_content=f'Key: {key}\nValue: {_value}',
        #     metadata=metadata,
        #     id=str(uuid.uuid4()),
        # ))

        # if len(documents) >= 5000:
        #     vector_store.add_documents(documents=documents)
        #     documents = []
    break

# if len(documents) > 0:
#     vector_store.add_documents(documents=documents)