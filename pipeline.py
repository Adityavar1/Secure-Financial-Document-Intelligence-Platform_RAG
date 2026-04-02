import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import DOCUMENTS_DIR, CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DB_DIR, MODEL_NAME, TEMPERATURE, NUM_RETRIEVED_DOCS

def load_documents():
    all_docs = []

    for file in os.listdir(DOCUMENTS_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCUMENTS_DIR, file))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file

            all_docs.extend(docs)

    return all_docs


def create_vector_store():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embedding = OpenAIEmbeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=VECTOR_DB_DIR
    )

    return vectorstore


def load_vector_store():
    if os.path.exists(VECTOR_DB_DIR):
        return Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=OpenAIEmbeddings()
        )
    return None


def create_qa_chain(vectorstore):

    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": NUM_RETRIEVED_DOCS}
    )

    template = """You are a financial research assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:
- Provide key insights
- Highlight risks or trends
- Use supporting evidence
"""

    PROMPT = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain