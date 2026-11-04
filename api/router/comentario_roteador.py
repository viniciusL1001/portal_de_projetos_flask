from flask import Blueprint


class ComentarioRoteador:
    def __init__(self, jwt_middleware, comentario_middleware, comentario_control):
        self.__jwt = jwt_middleware
        self.__middleware = comentario_middleware
        self.__control = comentario_control
        self.__blueprint = Blueprint("comentario", __name__)

    def create_routes(self):
        bp = self.__blueprint

        @bp.route("", methods=["POST"])
        @bp.route("/", methods=["POST"])
        @self.__jwt.validate_token
        @self.__middleware.validate_body
        def store():
            return self.__control.store()

        @bp.route("", methods=["GET"])
        @bp.route("/", methods=["GET"])
        def index():
            return self.__control.index()

        @bp.route("/projeto/<int:idProjeto>", methods=["GET"])
        def showByProjeto(idProjeto):
            return self.__control.showByProjeto(idProjeto)

        @bp.route("/<int:idComentario>", methods=["GET"])
        def show(idComentario):
            return self.__control.show(idComentario)

        @bp.route("/<int:idComentario>", methods=["PUT"])
        @self.__jwt.validate_token
        @self.__middleware.validate_body
        def update(idComentario):
            return self.__control.update(idComentario)

        @bp.route("/<int:idComentario>", methods=["DELETE"])
        @self.__jwt.validate_token
        def destroy(idComentario):
            return self.__control.destroy(idComentario)

        return bp
