from flask import request, jsonify


class ImagemControl:
    def __init__(self, service):
        self.__service = service

    def store(self):
        caminho = self.__service.salvar(
            request.get_data(), request.headers.get("Content-Type")
        )
        return jsonify({
            "success": True,
            "message": "Imagem enviada com sucesso.",
            "data": {"imagem": caminho}
        }), 201
