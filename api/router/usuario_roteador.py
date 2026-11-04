from flask import Blueprint


class UsuarioRoteador:
    def __init__(self, jwt_middleware, usuario_middleware, usuario_control):
        self.__jwt = jwt_middleware
        self.__middleware = usuario_middleware
        self.__control = usuario_control
        self.__blueprint = Blueprint("usuario", __name__)

    def create_routes(self):
        bp = self.__blueprint

        @bp.route("", methods=["POST"])
        @bp.route("/", methods=["POST"])
        @self.__middleware.validate_body
        def store():
            return self.__control.store()

        @bp.route("/login", methods=["POST"])
        @self.__middleware.validate_login_body
        def login():
            return self.__control.login()

        @bp.route("", methods=["GET"])
        @bp.route("/", methods=["GET"])
        @self.__jwt.validate_token
        def index():
            return self.__control.index()

        @bp.route("/me", methods=["GET"])
        @self.__jwt.validate_token
        def me():
            return self.__control.me()

        @bp.route("/<int:idUsuario>", methods=["GET"])
        @self.__jwt.validate_token
        def show(idUsuario):
            return self.__control.show(idUsuario)

        @bp.route("/<int:idUsuario>", methods=["PUT"])
        @self.__jwt.validate_token
        @self.__middleware.validate_own_account
        @self.__middleware.validate_update_body
        def update(idUsuario):
            return self.__control.update(idUsuario)

        @bp.route("/<int:idUsuario>", methods=["DELETE"])
        @self.__jwt.validate_token
        @self.__middleware.validate_own_account
        def destroy(idUsuario):
            return self.__control.destroy(idUsuario)

        return bp
