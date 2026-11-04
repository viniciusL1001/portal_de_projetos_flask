import os
import time
import secrets
from pathlib import Path
from dotenv import load_dotenv
import jwt


class MeuTokenJWT:
    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[2] / ".env")
        self._key = os.getenv("JWT_SECRET")
        if not self._key or self._key == "coloque_aqui_seu_segredo_jwt":
            raise RuntimeError("Configure JWT_SECRET com uma chave própria no arquivo .env.")
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
