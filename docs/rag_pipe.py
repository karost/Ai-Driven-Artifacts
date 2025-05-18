from langchain_community.document_loaders import DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# File Loading: Extract code (.py) and docs (.md, .txt)
file_extensions = ["py", "md", "txt"]
docs = []
path = "/home/thanit/projects/labs/rag/saleor"

for ext in file_extensions:
    logger.info(f"Loading .{ext} files...")
    loader = DirectoryLoader(
        path=path,
        glob=f"**/*.{ext}",
        show_progress=True
    )
    try:
        loaded_docs = loader.load()
        logger.info(f"Loaded {len(loaded_docs)} .{ext} documents")
        docs.extend(loaded_docs)
    except Exception as e:
        logger.error(f"Error loading .{ext} documents: {e}")

# Filter empty or invalid documents
docs = [doc for doc in docs if doc.page_content and doc.page_content.strip()]
logger.info(f"Filtered to {len(docs)} valid documents")

if not docs:
    logger.warning("No documents loaded. Check if directory contains .py, .md, or .txt files.")
    raise ValueError("No valid documents loaded. Check directory content or file formats.")

# Chunking: Split documents into semantic chunks
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    chunker = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
    chunks = chunker.split_documents(docs)
    logger.info(f"Created {len(chunks)} chunks")
    
    # Filter empty or invalid chunks
    chunks = [chunk for chunk in chunks if chunk.page_content and chunk.page_content.strip()]
    logger.info(f"Filtered to {len(chunks)} valid chunks")
    
    if not chunks:
        raise ValueError("No valid chunks to embed. Verify document content or chunking process.")
except Exception as e:
    logger.error(f"Error during chunking: {e}")
    raise

# Vector Store: Embed chunks and store in Chroma
try:
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    logger.info("Embedded chunks and stored in vector database")
except Exception as e:
    logger.error(f"Error creating vector store: {e}")
    raise

# Retriever: Fetch top-5 chunks with similarity threshold
try:
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.3}
    )
    logger.info("Configured retriever")
except Exception as e:
    logger.error(f"Error configuring retriever: {e}")
    raise

# Prompt Template: Restrict LLM to context
try:
    prompt_template = PromptTemplate.from_template(
        """
        You are a coding assistant. Answer using ONLY the provided context, focusing on code and technical details. If the context is insufficient, say "I don’t know."
        Context: {context}
        Question: {question}
        Answer:
        """
    )
    logger.info("Configured prompt template")
except Exception as e:
    logger.error(f"Error configuring prompt: {e}")
    raise

# Ollama Integration: Connect to LLM server
try:
    llm = OllamaLLM(
        model="qwen2.5-coder:14b",
        base_url="http://172.20.10.2:11434",
        temperature=0.7,
        num_predict=4096
    )
    logger.info("Connected to Ollama LLM")
except Exception as e:
    logger.error(f"Error connecting to Ollama: {e}")
    raise

# RAG Chain: Assemble pipeline
try:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )
    logger.info("Assembled RAG pipeline")
except Exception as e:
    logger.error(f"Error assembling RAG pipeline: {e}")
    raise

# Test Pipeline
try:
    response = qa_chain.invoke({"query": "Add logging to the payment microservice"})
    logger.info(f"Query response: {response['result']}")
except Exception as e:
    logger.error(f"Error running RAG pipeline: {e}")
