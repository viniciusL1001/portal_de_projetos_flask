from functools import wraps
from flask import request, jsonify, g
from api.http.meu_token_jwt import MeuTokenJWT


class JwtMiddleware:
    def validate_token(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = MeuTokenJWT()
            autenticado = token.validar_token(request.headers.get("Authorization"))
            payload = token.payload or {}
            id_usuario = payload.get("idUsuario")
            if not autenticado or type(id_usuario) is not int or id_usuario <= 0:
                return jsonify({
                    "success": False,
                    "message": "Token inválido.",
                    "error": {"message": "Faça login novamente."}
                }), 401
            g.usuario_autenticado = {"idUsuario": id_usuario}
            return func(*args, **kwargs)
        return wrapper
