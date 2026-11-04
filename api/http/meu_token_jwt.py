import os
import time
import secrets
import jwt


class MeuTokenJWT:
    def __init__(self):
        # Pode configurar JWT_SECRET no ambiente, sem precisar de arquivo .env.
        self._key = os.environ.get(
            "JWT_SECRET", "portal-de-projetos-flask-chave-local-altere-antes-de-publicar"
        )
        self._alg = "HS256"
        self._iss = "http://localhost"
        self._aud = "http://localhost"
        self._sub = "acesso_sistema"
        self._duracao_token = 3600 * 24 * 60
        self.payload = None

    def gerar_token(self, claims):
        agora = int(time.time())
        payload = {
            "iss": self._iss,
            "aud": self._aud,
            "sub": self._sub,
            "iat": agora,
            "exp": agora + self._duracao_token,
            "nbf": agora,
            "jti": secrets.token_hex(16),
            "email": claims["email"],
            "name": claims["name"],
            "idUsuario": claims["idUsuario"]
        }
        return jwt.encode(payload, self._key, algorithm=self._alg)

    def validar_token(self, autorizacao):
        if not autorizacao:
            return False
        token = autorizacao.removeprefix("Bearer ").strip()
        try:
            self.payload = jwt.decode(
                token, self._key, algorithms=[self._alg],
                audience=self._aud, issuer=self._iss
            )
            return self.payload.get("sub") == self._sub
        except jwt.InvalidTokenError:
            return False
