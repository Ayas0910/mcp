import sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

vector = embeddings.embed_query("I love to build the agentic ai system")

print("Type       :",type(vector).__name__)
print("Dimension  :",len(vector))
print()

print("Last five embedding values:",[round(number,4) for number in vector[:5]])
print()