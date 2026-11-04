from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse


class ComentarioMiddleware:
    def validate_body(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            comentario = (request.get_json(silent=True) or {}).get("comentario")
            if not isinstance(comentario, dict) or not comentario.get("texto"):
                raise ErrorResponse(400, "O texto do comentário é obrigatório.")
            usuario = comentario.get("usuario")
            projeto = comentario.get("projeto")
            if not isinstance(usuario, dict) or type(usuario.get("idUsuario")) is not int or usuario["idUsuario"] <= 0:
                raise ErrorResponse(400, "O campo usuario.idUsuario é obrigatório.")
            if not isinstance(projeto, dict) or type(projeto.get("idProjeto")) is not int or projeto["idProjeto"] <= 0:
                raise ErrorResponse(400, "O campo projeto.idProjeto é obrigatório.")
            return func(*args, **kwargs)
        return wrapper
