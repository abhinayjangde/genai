from dotenv import load_dotenv
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from pprint import pprint
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


"""
pdf_path = Path().cwd().joinpath("english.pdf")
loader = PyMuPDF4LLMLoader(pdf_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)
"""

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview",output_dimensionality=1536)

"""
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    collection_name="leaning_langchain",
    url="http://localhost:6333",
    embedding=embeddings
)
"""

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