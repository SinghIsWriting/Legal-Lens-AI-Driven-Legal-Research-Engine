from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader



# def extract_text_from_pdf(path):
#     # Load all PDFs from a directory
#     loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyPDFLoader)
#     documents = loader.load()
#     return documents

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    "2_Harry Potter and the  Chamber of Secrets.pdf",
)

data =loader.load()

print(data[35])