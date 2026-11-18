from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

HERE = Path(__file__).parent

load_dotenv()

#create the model
model = ChatOpenAI(model = "gpt-4o-mini",temperature = 0)

#create the embedding model
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

#create the list of documents to pass into the chunk
documents = [
    Document(page_content=doc.read_text(),metadata={"source":doc.name})
    for doc in (HERE/"data").glob("*.md")
]

#now I am going to create the chunks
chunks = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 30
).split_documents(documents)

#now create the vector store
store = Chroma.from_documents(
    chunks,
    embeddings,
    collection_name = "library_vector"
)

#now I am going to create the retriever
retriever = store.as_retriever(search_kwargs={"k":3})

#when sometimes user ask question that not in the vector still our
#application try to answer to overcome that problem what we need to do is
#we create one prompt template that works as only give correct answer otherwise it gives
#the no answer available for that I use the prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a support agent. Answer only from the context below. "
     "If the context does not cover the question, say you do not have that "
     "information and offer to connect a human. Keep it to three lines.\n\n"
     "Context:\n{context}"
         ),
        ("human","{question}")
    ]
)

#chat prompt template only accept the string not accept the document object so we need format converter
def format_convert(found):
    "In vector db we get it in the document object form but our chatprompt template need it in the str so we convert it here"
    return "\n\n".join(
        f"[{doc.metadata['source']}] : {doc.page_content}"
        for doc in found
    )


#now I write all the question in the list
questions = [

    # Membership questions
    "How much does library membership cost?",
    "Can a 17-year-old join the library?",

    # Borrowing questions
    "How many books can I borrow?",
    "Can I keep a book for 20 days?",
    "Can I borrow reference books?",

    # Fine questions
    "What happens if I return a book late?",
    "How much do I need to pay for a damaged book?",

    # Unsupported question
    "Does the library provide free Wi-Fi?"
]

chain = (
    {
        "context": retriever | format_convert,
        "question": RunnablePassthrough()
    }
    
    | prompt

    | model

    | StrOutputParser()
    
    )

for question in questions:
    print(f"Q: {question}")
    print(f"A: {chain.invoke(question)}")
    print("-"*100)
