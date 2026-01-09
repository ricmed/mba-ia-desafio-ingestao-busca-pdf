import sys
import os

# Adiciona o diretório src ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from search import search_prompt

def main():
    """CLI interativo para fazer perguntas sobre o PDF"""
    print("=" * 60)
    print("Sistema de Busca Semântica - Chat com PDF")
    print("=" * 60)
    print("Digite 'sair' ou 'exit' para encerrar o chat.\n")
    
    while True:
        try:
            # Solicita a pergunta do usuário
            pergunta = input("PERGUNTA: ").strip()
            
            # Verifica se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando o chat. Até logo!")
                break
            
            # Verifica se a pergunta não está vazia
            if not pergunta:
                print("Por favor, digite uma pergunta.\n")
                continue
            
            # Busca e gera resposta
            print("\nProcessando...")
            resposta = search_prompt(pergunta)
            
            # Exibe a resposta
            print(f"RESPOSTA: {resposta}\n")
            print("-" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\n\nEncerrando o chat. Até logo!")
            break
        except Exception as e:
            print(f"\nErro: {str(e)}\n")
            print("-" * 60)
            print()

if __name__ == "__main__":
    main()