from flask import jsonify, request, g


class ProjetoControl:
    def __init__(self, service):
        self.__service = service

    def store(self):
        projeto = self.__service.createService(
            request.json["projeto"], g.usuario_autenticado["idUsuario"]
        )
        return jsonify({
            "success": True, "message": "Criado com sucesso",
            "data": {"projeto": projeto}
        }), 200

    def index(self):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso",
            "data": {"message": self.__service.findAllService()}
        }), 200

    def show(self, idProjeto):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso",
            "data": {"message": self.__service.findByIdService(idProjeto)}
        }), 200

    def update(self, idProjeto):
        projeto = request.json["projeto"]
        self.__service.updateService(
            idProjeto, projeto, g.usuario_autenticado["idUsuario"]
        )
        return jsonify({
            "success": True, "message": "Atualizado com sucesso",
            "data": {"projeto": {"idProjeto": idProjeto, "titulo": projeto["titulo"]}}
        }), 200

    def destroy(self, idProjeto):
        excluiu = self.__service.deleteService(
            idProjeto, g.usuario_autenticado["idUsuario"]
        )
        if not excluiu:
            return jsonify({"success": False, "message": "Projeto não encontrado."}), 404
        return jsonify({"success": True, "message": "Excluído com sucesso"}), 200
