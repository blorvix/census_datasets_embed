import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# from transformers import AutoTokenizer

# Load the tokenizer for the nomic-embed-text model
# tokenizer = AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1")

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
vector_store = Chroma(
    collection_name="census_datasets",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db/full",  # Where to save data locally, remove if not necessary
)

documents = []

INVALID_FIELDS = ['for', 'in', 'ucgid']

with open('data/census_data_level.json', 'r') as file:
    census_data = json.load(file)

for i in range(len(census_data)):
# for i in range(0, 100):
    index = i + 1
    item = census_data[i]
    print(i, len(census_data))
    # if 'var_build_level' in item:
    #     continue
    variables_json_path = 'census_variables/' + (item['category'].replace('/', '_')) + '.json'
    with open(variables_json_path, 'r') as file:
        variables_data = json.load(file)
        variables = [(name, value['label'], value.get('predicateType','')) for name, value in variables_data['variables'].items() if name not in INVALID_FIELDS]
        item['variables'] = json.dumps(variables)
        
        cut_label = lambda value, comp_len: value if len(value) <= comp_len * 2 else value[:comp_len] + '...' + value[-comp_len:]
        get_text = lambda variables: 'Title: {title}\nCategory: {category}\nDescription: {description}\nFields: {fields}'.format(
            title=item['title'],
            description=item['description'],
            category=(item['category'].replace('/', ' ') + ' ') * 20,
            fields=variables
        )
        # get_text = lambda variables: 'Title: {title}\nCategory: {category}\nDescription: {description}'.format(
        #     title=item['title'],
        #     description=item['description'],
        #     category=(item['category'].replace('/', ' ') + ' ') * 20,
        # )
        # get_token_count = lambda text: len(tokenizer.tokenize(text))
        # is_good_text = lambda text: get_token_count(text) <= 8000

        def get_variables_text(build_type):
            if build_type == 0: return '\n'.join([v[0] + ': ' + v[1] + ' ' + v[2] for v in variables])
            if build_type == 1: return '\n'.join([v[0] + ': ' + v[1] for v in variables])
            if build_type == 2: return '\n'.join([v[0] + ': ' + cut_label(v[1], 80) for v in variables])
            if build_type == 3: return '\n'.join([v[0] + ': ' + cut_label(v[1], 60) for v in variables])
            if build_type == 4: return '\n'.join([v[0] + ': ' + cut_label(v[1], 40) for v in variables])
            if build_type == 5: return '\n'.join([v[0] + ': ' + cut_label(v[1], 30) for v in variables])
            if build_type == 6: return ' '.join([v[0] for v in variables])
            if build_type >= 7: return ' '.join([variables[i][0] for i in range(min(len(variables), 1800 - 200 * (build_type - 7)))])

        # def build_doc_content():
        #     for i in range(15):
        #         text = get_text(get_variables_text(i))
        #         if is_good_text(text):
        #             return i, text
                
        #     print(item, len(variables), get_token_count(get_text(get_variables_text(14))))
        #     return -1, None

        # var_build_level, text = build_doc_content()
        # item['var_build_level'] = var_build_level
        # with open('data/census_data_level.json', 'w') as file:
        #     json.dump(census_data, file, indent=2)

        if item['year'] is None:
            del item['year']

        text = get_text(get_variables_text(item['var_build_level']))
        if text is not None:
            documents.append(Document(
                page_content=text,
                metadata=item,
                id=index,
            ))

vector_store.add_documents(documents=documents)