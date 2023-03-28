import requests
import nltk
import os

from parser.file.bulk import SimpleDirectoryReader
from parser.schema.base import Document
from parser.open_ai_func import call_openai_api
from parser.token_func import group_split
from celery import current_task


import string
import zipfile
import shutil

try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except FileExistsError:
    pass
def generate_random_string(length):
    return ''.join([string.ascii_letters[i % 52] for i in range(length)])



def ingest_worker(self, directory, formats, name_job, filename, user):
    # directory = 'inputs' or 'temp'
    # formats = [".rst", ".md"]
    input_files = None
    recursive = True
    limit = None
    exclude = True
    # name_job = 'job1'
    # filename = 'install.rst'
    # user = 'local'
    sample = False
    token_check = True
    min_tokens = 150
    max_tokens = 1250
    full_path = directory + '/' + user + '/' + name_job
    # check if API_URL env variable is set
    if not os.environ.get('API_URL'):
        url = 'http://localhost:5001/api/download'
    else:
        url = os.environ.get('API_URL') + '/api/download'
    file_data = {'name': name_job, 'file': filename, 'user': user}
    response = requests.get(url, params=file_data)
    file = response.content

    if not os.path.exists(full_path):
        os.makedirs(full_path)
    with open(full_path + '/' + filename, 'wb') as f:
        f.write(file)

    #check if file is .zip and extract it
    if filename.endswith('.zip'):
        with zipfile.ZipFile(full_path + '/' + filename, 'r') as zip_ref:
            zip_ref.extractall(full_path)
        os.remove(full_path + '/' + filename)


    import time
    self.update_state(state='PROGRESS', meta={'current': 1})

    raw_docs = SimpleDirectoryReader(input_dir=full_path, input_files=input_files, recursive=recursive,
                                     required_exts=formats, num_files_limit=limit,
                                     exclude_hidden=exclude).load_data()
    raw_docs = group_split(documents=raw_docs, min_tokens=min_tokens, max_tokens=max_tokens, token_check=token_check)

    docs = [Document.to_langchain_format(raw_doc) for raw_doc in raw_docs]

    call_openai_api(docs, full_path, self)
    self.update_state(state='PROGRESS', meta={'current': 100})

    if sample == True:
        for i in range(min(5, len(raw_docs))):
            print(raw_docs[i].text)

    # get files from outputs/inputs/index.faiss and outputs/inputs/index.pkl
    # and send them to the server (provide user and name in form)
    if not os.environ.get('API_URL'):
        url = 'http://localhost:5001/api/upload_index'
    else:
        url = os.environ.get('API_URL') + '/api/upload_index'
    file_data = {'name': name_job, 'user': user}
    files = {'file_faiss': open(full_path + '/index.faiss', 'rb'),
             'file_pkl': open(full_path + '/index.pkl', 'rb')}
    response = requests.post(url, files=files, data=file_data)

    #deletes remote
    if not os.environ.get('API_URL'):
        url = 'http://localhost:5001/api/delete_old?path=' + 'inputs/' + user + '/' + name_job
    else:
        url = os.environ.get('API_URL') + '/api/delete_old?path=' + 'inputs/' + user + '/' + name_job
    response = requests.get(url)
    # delete local
    shutil.rmtree(full_path)

    return {'directory': directory, 'formats': formats, 'name_job': name_job, 'filename': filename, 'user': user, 'limited': False}
