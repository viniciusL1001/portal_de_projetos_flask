import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge

from api.database.mysql_database import MysqlDatabase
from api.utils.error_response import ErrorResponse
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.usuario_middleware import UsuarioMiddleware
from api.middleware.projeto_middleware import ProjetoMiddleware
from api.middleware.comentario_middleware import ComentarioMiddleware
from api.dao.usuario_dao import UsuarioDAO
from api.dao.projeto_dao import ProjetoDAO
from api.dao.comentario_dao import ComentarioDAO
from api.service.usuario_service import UsuarioService
from api.service.projeto_service import ProjetoService
from api.service.comentario_service import ComentarioService
from api.service.imagem_service import ImagemService
from api.control.usuario_control import UsuarioControl
from api.control.projeto_control import ProjetoControl
from api.control.comentario_control import ComentarioControl
from api.control.imagem_control import ImagemControl
from api.router.usuario_roteador import UsuarioRoteador
from api.router.projeto_roteador import ProjetoRoteador
from api.router.comentario_roteador import ComentarioRoteador


class Server:
    def __init__(self, porta=8000):
        self.__porta = porta
        self.__app = Flask(__name__, static_folder="static", static_url_path="")
        self.__app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
        CORS(self.__app, resources={r"/*": {"origins": "*"}})

    def init(self):
        load_dotenv(Path(__file__).resolve().parent / '.env')
        # Mesma base de dados usada pela API Node.js.
        self.__database = MysqlDatabase(
            pool_name="pool_portal",
            pool_size=10,
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "portal_de_projetos"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        self.__database.connect()

        jwt_middleware = JwtMiddleware()
        usuario_dao = UsuarioDAO(self.__database)
        projeto_dao = ProjetoDAO(self.__database)
        comentario_dao = ComentarioDAO(self.__database)

        usuario_service = UsuarioService(usuario_dao)
        projeto_service = ProjetoService(projeto_dao, usuario_dao)
        comentario_service = ComentarioService(comentario_dao, projeto_dao, usuario_dao)

        usuario_router = UsuarioRoteador(
            jwt_middleware, UsuarioMiddleware(),
            UsuarioControl(usuario_service)
        )
        projeto_router = ProjetoRoteador(
            jwt_middleware, ProjetoMiddleware(),
            ProjetoControl(projeto_service),
            ImagemControl(ImagemService())
        )
        comentario_router = ComentarioRoteador(
            jwt_middleware, ComentarioMiddleware(),
            ComentarioControl(comentario_service)
        )

        self.__app.register_blueprint(usuario_router.create_routes(), url_prefix="/api/usuarios")
        self.__app.register_blueprint(projeto_router.create_routes(), url_prefix="/api/projetos")
        self.__app.register_blueprint(comentario_router.create_routes(), url_prefix="/api/comentarios")

        self.__error_middleware()

    def __error_middleware(self):
        @self.__app.errorhandler(Exception)
        def tratar_erro(error):
            if isinstance(error, ErrorResponse):
                return jsonify({
                    "success": False,
                    "message": error.args[0],
                    "error": error.error or {"message": error.args[0]}
                }), error.httpCode

            if isinstance(error, RequestEntityTooLarge):
                return jsonify({
                    "success": False,
                    "message": "Imagem muito grande.",
                    "error": {"message": "O tamanho máximo é 2 MB."}
                }), 413

            if isinstance(error, HTTPException):
                return jsonify({
                    "success": False,
                    "message": error.description,
                    "error": {"message": error.description}
                }), error.code

            print("Erro interno:", error)
            return jsonify({
                "success": False,
                "message": "Ocorreu um erro interno no servidor.",
                "error": {"message": "Erro interno. Confira o terminal."}
            }), 500

    def run(self):
        print(f"Server rodando em http://localhost:{self.__porta}/Login.html")
        self.__app.run(port=self.__porta, debug=False)
