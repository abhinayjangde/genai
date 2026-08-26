
1. create a python project using `uv` and add dependencies

```bash
uv init .
uv add python-dotenv langchain_text_splitters langchain_pymupdf4llm
uv add langchain_qdrant langchain_google_genai langchain_core

# add .env file
GEMINI_API_KEY=""

```

2. pdf document load and chunking

```python
from dotenv import load_dotenv
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

load_dotenv()

#1. load pdf file
pdf_path = Path().cwd().joinpath("english.pdf")
loader = PyMuPDF4LLMLoader(pdf_path)

docs = loader.load()

#2. split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)
```

3. Setup the qdrant db on docker and create a collection on qdrant db from dashboard `http://localhost:6333/dashboard`

```bash
services:
  qdrant:
    image: qdrant/qdrant
    container_name: qdrant
    ports:
      - 6333:6333
```

4. create vector embeddings and store in vector db

```python
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview",output_dimensionality=1536)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    collection_name="leaning_langchain",
    url="http://localhost:6333",
    embedding=embeddings
)

```

5. retrive relevant chunks and product ai response

```python


retriver = QdrantVectorStore.from_existing_collection(
    collection_name="leaning_langchain",
    url="http://localhost:6333",
    embedding=embeddings
)

relevant_chunks = retriver.similarity_search(
    query="what is the first 5 words on flash card give with there hindi meaning?"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    temperature=1.0
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an helpful AI Assistant who responds based on the available context.
            context:
                {relevant_chunks}"""),
      ("human", "{query}")

    ]
)


chain = prompt | llm

result = chain.invoke({
    "query":"what is the first 5 words on flash card give with there hindi meaning?",
    "relevant_chunks": relevant_chunks
})

print(result.content)
```