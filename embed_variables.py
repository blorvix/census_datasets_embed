import uuid
import requests
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
vector_store = Chroma(
    collection_name="census_variables",
    embedding_function=embeddings,
    persist_directory="./chroma_census_db/census_variables",
)

documents = []

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

total = 0

for i in range(0, len(census_data)):
    print('Checking dataset', i)
    item = census_data[i]
    category = item['category']

    documents = []

    response = requests.get(item['variables_json_url'])
    variables = response.json()
    # variables_json_path = 'census_variables/' + (category.replace('/', '_')) + '.json'
    # with open(variables_json_path, 'r') as file:
        # variables = json.load(file)
        
    for name, values in variables['variables'].items():
        if name in ['for', 'in', 'ucgid']:
            continue
        text = f'name: {name}\n'
        for key, value in values.items():
            if key == 'values':
                continue
            if isinstance(value, dict):
                value = json.dumps(value)
            text += f'{key}: {value}\n'

        documents.append(Document(
            page_content=text,
            metadata={
                'category': category,
                'name': name
            },
            id=str(uuid.uuid4()),
        ))

    vector_store.add_documents(documents=documents)
    print('Added', i)

    break