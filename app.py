from server import Server
"""
Arquivo principal de inicialização do servidor Flask.

Responsabilidades:
- Cria a instância do servidor
- Inicializa todas as dependências (banco, middlewares, rotas)
- Inicia o servidor na porta especificada
"""
def main():
    try:
        server = Server(porta=8000)

        server.init()

        server.run()

        print("✅ Servidor iniciado com sucesso")
    except Exception as error:
        print("❌ Erro ao iniciar o servidor:", error)



main()