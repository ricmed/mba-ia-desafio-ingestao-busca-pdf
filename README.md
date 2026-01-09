# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e PostgreSQL

Sistema completo de ingestão e busca semântica de documentos PDF usando LangChain, PostgreSQL com extensão pgVector, e modelos de IA (OpenAI ou Google Gemini).

## 📋 Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- API Key da OpenAI ou Google Gemini
- Ambiente virtual Python (já criado como `.venv`)

## 🚀 Instalação

1. **Clone o repositório** (se ainda não tiver feito):
```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca-pdf
```

2. **Ative o ambiente virtual**:
```bash
source .venv/bin/activate
```

3. **Configure as variáveis de ambiente**:
   - Copie o arquivo `.env.example` para `.env` (se existir) ou crie um arquivo `.env` na raiz do projeto
   - Adicione suas chaves de API:
```env
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_openai_aqui

# Google Gemini Configuration (opcional)
GOOGLE_API_KEY=sua_chave_google_aqui

# Provider Selection: "openai" ou "gemini"
EMBEDDING_PROVIDER=openai
LLM_PROVIDER=openai

# PDF Path (padrão: document.pdf na raiz do projeto)
PDF_PATH=document.pdf

# Database Configuration (padrões já configurados)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

4. **Coloque o arquivo PDF** na raiz do projeto com o nome `document.pdf` (ou ajuste a variável `PDF_PATH` no `.env`)

## 🐳 Executando o Banco de Dados

Suba o PostgreSQL com pgVector usando Docker Compose:

```bash
docker compose up -d
```

Aguarde alguns segundos para o banco estar pronto. O serviço `bootstrap_vector_ext` criará automaticamente a extensão `vector` no PostgreSQL.

Para verificar se está rodando:
```bash
docker compose ps
```

## 📥 Ingestão do PDF

Execute o script de ingestão para processar o PDF e armazenar os embeddings no banco de dados:

```bash
python src/ingest.py
```

O script irá:
- Carregar o PDF
- Dividir em chunks de 1000 caracteres com overlap de 150
- Gerar embeddings usando o modelo configurado
- Armazenar os vetores no PostgreSQL

**Nota**: Se você já executou a ingestão anteriormente e quer reprocessar, pode ser necessário limpar a tabela existente ou usar um nome de coleção diferente.

## 💬 Chat Interativo

Execute o chat para fazer perguntas sobre o conteúdo do PDF:

```bash
python src/chat.py
```

Exemplo de uso:
```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Para sair do chat, digite `sair`, `exit`, `quit` ou `q`.

## 🔧 Configuração de Modelos

### OpenAI
- **Embeddings**: `text-embedding-3-small`
- **LLM**: `gpt-4o-mini` (o modelo `gpt-5-nano` mencionado não existe, usando `gpt-4o-mini` como alternativa)

### Google Gemini
- **Embeddings**: `models/embedding-001`
- **LLM**: `gemini-2.5-flash-lite`

Para alternar entre providers, ajuste as variáveis `EMBEDDING_PROVIDER` e `LLM_PROVIDER` no arquivo `.env`.

## 📁 Estrutura do Projeto

```
├── docker-compose.yml          # Configuração do PostgreSQL com pgVector
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (não versionado)
├── document.pdf                # PDF para ingestão
├── src/
│   ├── ingest.py              # Script de ingestão do PDF
│   ├── search.py              # Busca semântica e geração de resposta
│   └── chat.py                # CLI interativo para perguntas
└── README.md                   # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **LangChain**: Framework para aplicações com LLMs
- **PostgreSQL + pgVector**: Banco de dados vetorial
- **Docker & Docker Compose**: Containerização do banco de dados
- **OpenAI API**: Modelos de embeddings e LLM
- **Google Gemini API**: Alternativa para embeddings e LLM

## 📝 Notas Importantes

1. **Primeira execução**: Certifique-se de executar `docker compose up -d` antes de rodar a ingestão
2. **Reingestão**: Se precisar reprocessar o PDF, você pode precisar limpar os dados anteriores ou ajustar o código
3. **Custos**: O uso de APIs da OpenAI e Google Gemini pode gerar custos. Monitore seu uso
4. **Modelo LLM**: O modelo `gpt-5-nano` mencionado no requisito não existe. O código usa `gpt-4o-mini` como alternativa compatível

## 🐛 Solução de Problemas

### Erro de conexão com o banco
- Verifique se o Docker está rodando: `docker compose ps`
- Verifique se o PostgreSQL está saudável: `docker compose logs postgres`

### Erro de API Key
- Verifique se o arquivo `.env` existe e contém as chaves corretas
- Certifique-se de que as chaves não têm espaços extras

### Erro ao importar módulos
- Ative o ambiente virtual: `source .venv/bin/activate`
- Verifique se todas as dependências estão instaladas: `pip list`

## 📄 Licença

Este projeto foi desenvolvido como parte do desafio do MBA em Engenharia de Software com IA.