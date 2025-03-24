import uuid
import requests
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

with open('data/census_datasets_parts.json', 'r') as file:
    census_data = json.load(file)

for part_number in range(11, 21):
    print('Checking part', part_number)

    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
    vector_store = Chroma(
        collection_name=f"census_variables_{part_number}",
        embedding_function=embeddings,
        persist_directory=f"./chroma_census_db/census_variables_{part_number}",
    )

    documents = []

    total = 0

    for category, dataset in census_data.items():
        if dataset['variables_embed_part'] != part_number:
            continue

        print('Checking dataset', category)

        documents = []

        # response = requests.get(item['variables_json_url'])
        # variables = response.json()
        variables_json_path = 'census_variables/' + (category.replace('/', '_')) + '.json'
        with open(variables_json_path, 'r') as file:
            variables = json.load(file)
            
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

                if len(documents) >= 5000:
                    vector_store.add_documents(documents=documents)
                    documents = []

        if len(documents) > 0:
            vector_store.add_documents(documents=documents)
        print('Added', category)

    print('Finished part', part_number)