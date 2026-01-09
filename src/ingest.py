import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Configurações - sempre resolve o caminho do PDF relativo à raiz do projeto
pdf_path_env = os.getenv("PDF_PATH", "document.pdf")

# Sempre resolve em relação à raiz do projeto
project_root = Path(__file__).parent.parent
PDF_PATH = str(project_root / pdf_path_env)
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rag")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# String de conexão PostgreSQL
CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_embeddings():
    """Retorna o modelo de embeddings baseado no provider configurado"""
    if EMBEDDING_PROVIDER == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    else:  # openai
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        return OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)

def ingest_pdf():
    """Ingere o PDF, divide em chunks, cria embeddings e salva no PostgreSQL"""
    print(f"Carregando PDF: {PDF_PATH}")
    
    # Verifica se o arquivo existe
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {PDF_PATH}")
    
    # Carrega o PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    
    print(f"PDF carregado. Total de páginas: {len(documents)}")
    
    # Divide em chunks: 1000 caracteres com overlap de 150
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"Documento dividido em {len(chunks)} chunks")
    
    # Obtém o modelo de embeddings
    embeddings = get_embeddings()
    print(f"Usando embeddings: {EMBEDDING_PROVIDER}")
    
    # Conecta ao PostgreSQL e salva os vetores
    print("Conectando ao PostgreSQL...")
    vectorstore = PGVector(
        embeddings=embeddings,
        connection=CONNECTION_STRING,
        use_jsonb=True,
        collection_name="pdf_documents",
    )
    
    print("Salvando chunks no banco de dados...")
    vectorstore.add_documents(chunks)
    
    print("Ingestão concluída com sucesso!")


if __name__ == "__main__":
    ingest_pdf()