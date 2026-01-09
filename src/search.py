import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

# Configurações
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
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

def get_llm():
    """Retorna o modelo LLM baseado no provider configurado"""
    if LLM_PROVIDER == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key)
    else:  # openai
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        return ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0)

def search_prompt(question):
    """
    Busca os documentos mais relevantes e gera resposta usando LLM
    
    Args:
        question: Pergunta do usuário
        
    Returns:
        Resposta gerada pela LLM baseada no contexto encontrado
    """
    if not question:
        return "Por favor, forneça uma pergunta."
    
    try:
        # Obtém embeddings e conecta ao banco
        embeddings = get_embeddings()
        vectorstore = PGVector(
            embeddings=embeddings,
            connection=CONNECTION_STRING,
            use_jsonb=True,
            collection_name="pdf_documents",
        )
        
        # Busca os 10 documentos mais relevantes
        results = vectorstore.similarity_search_with_score(question, k=10)
        
        # Concatena o conteúdo dos documentos encontrados
        contexto = "\n\n".join([doc.page_content for doc, score in results])
        
        # Monta o prompt final
        prompt = PROMPT_TEMPLATE.format(
            contexto=contexto,
            pergunta=question
        )
        
        # Chama a LLM
        llm = get_llm()
        response = llm.invoke(prompt)
        
        # Extrai o conteúdo da resposta
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
            
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"