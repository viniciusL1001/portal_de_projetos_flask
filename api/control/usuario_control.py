from flask import jsonify, request, g


class UsuarioControl:
    def __init__(self, service):
        self.__service = service

    def store(self):
        usuario = request.json["usuario"]
        id_usuario = self.__service.createService(usuario)
        return jsonify({
            "success": True, "message": "Cadastro realizado com sucesso.",
            "data": {"usuario": id_usuario}
        }), 200

    def login(self):
        resultado = self.__service.loginService(request.json["usuario"])
        return jsonify({
            "success": True, "message": "Login efetuado com sucesso.",
            "data": resultado
        }), 200

    def index(self):
        return jsonify({
            "success": True, "message": "Busca executada com sucesso.",
            "data": {"usuarios": self.__service.findAllService()}
        }), 200

    def show(self, idUsuario):
        usuario = self.__service.findPublicByIdService(idUsuario)
        return jsonify({
            "success": True, "message": "Busca executada com sucesso.",
            "data": {"usuario": usuario}
        }), 200

    def me(self):
        usuario = self.__service.findByIdService(g.usuario_autenticado["idUsuario"])
        return jsonify({"success": True, "data": {"usuario": usuario}}), 200

    def update(self, idUsuario):
        usuario = request.json["usuario"]
        self.__service.updateService(idUsuario, usuario, g.usuario_autenticado["idUsuario"])
        return jsonify({
            "success": True, "message": "Atualizado com sucesso.",
            "data": {"usuario": {"idUsuario": idUsuario, "nomeUsuario": usuario["nomeUsuario"]}}
        }), 200

    def destroy(self, idUsuario):
        excluiu = self.__service.deleteService(idUsuario, g.usuario_autenticado["idUsuario"])
        if not excluiu:
            return jsonify({"success": False, "message": "Usuário não encontrado."}), 404
        return jsonify({"success": True, "message": "Excluído com sucesso."}), 200
