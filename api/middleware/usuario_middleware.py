from functools import wraps
from flask import request, g
from api.utils.error_response import ErrorResponse


class UsuarioMiddleware:
    def validate_body(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = (request.get_json(silent=True) or {}).get("usuario")
            if not isinstance(usuario, dict) or any(
                not usuario.get(chave) for chave in ("nomeUsuario", "email", "senha")
            ):
                raise ErrorResponse(400, "Informe nomeUsuario, email e senha.")
            return func(*args, **kwargs)
        return wrapper

    def validate_login_body(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = (request.get_json(silent=True) or {}).get("usuario")
            if not isinstance(usuario, dict) or not usuario.get("email") or not usuario.get("senha"):
                raise ErrorResponse(400, "Informe e-mail e senha.")
            return func(*args, **kwargs)
        return wrapper

    def validate_update_body(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = (request.get_json(silent=True) or {}).get("usuario")
            if not isinstance(usuario, dict) or not usuario.get("nomeUsuario") or not usuario.get("email"):
                raise ErrorResponse(400, "Informe nome e e-mail.")
            return func(*args, **kwargs)
        return wrapper

    def validate_own_account(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get("idUsuario") != g.usuario_autenticado["idUsuario"]:
                raise ErrorResponse(403, "Você só pode alterar sua própria conta.")
            return func(*args, **kwargs)
        return wrapper
