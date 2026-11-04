from flask import Blueprint


class ProjetoRoteador:
    def __init__(self, jwt_middleware, projeto_middleware, projeto_control, imagem_control):
        self.__jwt = jwt_middleware
        self.__middleware = projeto_middleware
        self.__control = projeto_control
        self.__imagem = imagem_control
        self.__blueprint = Blueprint("projeto", __name__)

    def create_routes(self):
        bp = self.__blueprint

        @bp.route("/imagem", methods=["POST"])
        @self.__jwt.validate_token
        def imagem():
            return self.__imagem.store()

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

        @bp.route("/<int:idProjeto>", methods=["GET"])
        def show(idProjeto):
            return self.__control.show(idProjeto)

        @bp.route("/<int:idProjeto>", methods=["PUT"])
        @self.__jwt.validate_token
        @self.__middleware.validate_body
        def update(idProjeto):
            return self.__control.update(idProjeto)

        @bp.route("/<int:idProjeto>", methods=["DELETE"])
        @self.__jwt.validate_token
        def destroy(idProjeto):
            return self.__control.destroy(idProjeto)

        return bp
