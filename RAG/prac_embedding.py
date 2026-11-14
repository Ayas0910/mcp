from langchain_core.documents import Document
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


DOCUMENT_PATH = Path(__file__).parent/"Data"
CHROMA_DATA = DOCUMENT_PATH/"data"


#import the environment variables for the .env file
load_dotenv()

#create the embedding model for to achieve the process of embedding
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")


#create the documents list to give to the chunk
documents = [
    Document(page_content = path.read_text(encoding="utf-8"),metadata = {"source":path.name})
    for path in DOCUMENT_PATH.glob("*.md")
]

#create the chunk to store in the vector db
chunks = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50
).split_documents(documents)

#create the vector db
store = Chroma.from_documents(
    documents = chunks,
    embedding =embeddings,
    collection_name = "superhero_db",
    persist_directory = str(CHROMA_DATA)
)

while(True):

    question = input("Ask a question related to superman,batman and spiderman:")
    print()
    results = store.similarity_search(question,k=3)

    for result in results:
        print(
            f"{result.metadata['source']} : "
            f"{result.page_content}"
        )
        print("*********")
    
    print("------------------------------------------------------")

