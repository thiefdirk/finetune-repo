from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
# from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders.text import TextLoader

from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import os
os.environ["OPENAI_API_KEY"] = 
# Load Data
# loader = UnstructuredFileLoader("state_of_the_union.txt")
# load json file directory
loader = TextLoader("C:\work/repo-20230321/finetune-repo\chat-your-data-master/all_files_merged_ansi.txt")
# loader = UnstructuredFileLoader("C:\work/repo-20230321/finetune-repo\chat-your-data-master/all_files_merged.csv")
raw_documents = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(raw_documents)


# Load Data to vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)


# Save vectorstore
with open("C:\work/repo-20230321/finetune-repo\chat-your-data-master/vectorstore_CSV.pkl", "wb") as f:
    pickle.dump(vectorstore, f)
