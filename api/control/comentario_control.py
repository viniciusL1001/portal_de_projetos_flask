from flask import jsonify, request, g


class ComentarioControl:
    def __init__(self, service):
        self.__service = service

    def store(self):
        id_comentario = self.__service.createService(
            request.json["comentario"], g.usuario_autenticado["idUsuario"]
        )
        return jsonify({
            "success": True, "message": "Criado com sucesso",
            "data": {"comentario": id_comentario}
        }), 200

    def index(self):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso",
            "data": {"resultado": self.__service.findAllService()}
        }), 200

    def show(self, idComentario):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso",
            "data": {"comentario": self.__service.findByIdService(idComentario)}
        }), 200

    def showByProjeto(self, idProjeto):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso.",
            "data": {"comentarios": self.__service.findByIdProjetoService(idProjeto)}
        }), 200

    def update(self, idComentario):
        comentario = request.json["comentario"]
        self.__service.updateService(
            idComentario, comentario, g.usuario_autenticado["idUsuario"]
        )
        return jsonify({
            "success": True, "message": "Comentario atualizado com sucesso",
            "data": {
                "idComentario": idComentario,
                "usuario": {"idUsuario": g.usuario_autenticado["idUsuario"]}
            }
        }), 200

    def destroy(self, idComentario):
        excluiu = self.__service.deleteService(
            idComentario, g.usuario_autenticado["idUsuario"]
        )
        if not excluiu:
            return jsonify({"success": False, "message": "Comentário não encontrado."}), 404
        return jsonify({"success": True, "message": "Excluído com sucesso"}), 200
