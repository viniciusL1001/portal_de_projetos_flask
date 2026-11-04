from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse


class ProjetoMiddleware:
    def validate_body(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            projeto = (request.get_json(silent=True) or {}).get("projeto")
            if not isinstance(projeto, dict):
                raise ErrorResponse(400, "O campo 'projeto' é obrigatório.")
            if not projeto.get("titulo") or not projeto.get("linkGitHub"):
                raise ErrorResponse(400, "Título e linkGitHub são obrigatórios.")
            usuario = projeto.get("usuario")
            if not isinstance(usuario, dict) or type(usuario.get("idUsuario")) is not int or usuario["idUsuario"] <= 0:
                raise ErrorResponse(400, "O campo usuario.idUsuario é obrigatório.")
            return func(*args, **kwargs)
        return wrapper
