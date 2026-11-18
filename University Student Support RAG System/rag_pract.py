import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

#I create the llm to answer the question
model = ChatOpenAI(model = "gpt-4o-mini",temperature = 0)

#create the embedding model to achieve the embedding process
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

#create the list to store the text inside it after that I make chunk from it
documents = [
    Document(page_content=doc.read_text(encoding="utf-8"), metadata={"source": doc.name})
    for doc in (Path(__file__).parent/"data").glob("*.md")
]

#Now create chunk from the documents
chunks = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=30
).split_documents(documents)

#now put the chunk into the chroma db
store = Chroma.from_documents(
    chunks,
    embeddings,
    collection_name = "university_student"
)

#now I need to create one interface retriever
retriever = store.as_retriever(search_kwargs={"k":3})

#now I create the questions here
questions = [
    "I have 70% attendance. Can I attend my semester examination?",
    "I failed one subject. What should I do?",
    "Can I apply for revaluation after 15 days?",
    "How are internal assessment marks calculated?",
    "I was sick for two weeks. Will my attendance shortage be automatically excused?",
    "Can I apply for revaluation of my internal assessment marks?",
    "I have 80% attendance, but I haven't registered for the examination. Can I write it?",
    "What is the revaluation fee if I want to apply for three subjects?",
    "Can I improve my internal marks after the semester examination?",
    "Does the university provide hostel fee refunds?"
]

#I create the prompt template so that with stop the hallucination understood
prompt = ChatPromptTemplate.from_messages([
    ("system",
    "Your are the helpfull assistant if the user question answer is not in "
    "not in the chroma then don't hallucinate just answer I don't have answer for this "
    "Please call someone from the university"
    "Content:\n{content}"
    ),
    ("human","{question}")
])

#I need to convert object into string because PromptTemplate don't accept object
#only accept string 
def format_convert(str):
    "this convert the vector db object into string"
    return "\n\n".join(
        f"[{question.metadata['source']}]:{question.page_content}"
        for question in str
    )

#now I need to create one chain to combine all these things
chain = (
    {
        "content": retriever | format_convert,
        "question": RunnablePassthrough()
    }

    | prompt

    | model

    | StrOutputParser()
)

#now I use the for loop to run the question one by one
for question in questions:
    print(f"Q:{question}")
    print(f"A:{chain.invoke(question)}")
    print("-"*150)