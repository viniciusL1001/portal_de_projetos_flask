import re
from api.model.usuario import Usuario
from api.http.meu_token_jwt import MeuTokenJWT
from api.utils.error_response import ErrorResponse


class UsuarioService:
    def __init__(self, usuario_dao):
        self.__usuarioDAO = usuario_dao

    @staticmethod
    def __validar_usuario(dados, exigir_senha=True):
        nome = dados.get("nomeUsuario")
        email = dados.get("email")
        senha = dados.get("senha")
        if not isinstance(nome, str) or len(nome.strip()) < 4 or len(nome) > 100:
            raise ErrorResponse(400, "Nome de usuário deve ter entre 4 e 100 caracteres.")
        if not isinstance(email, str) or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()):
            raise ErrorResponse(400, "E-mail inválido.")
        if exigir_senha or senha is not None:
            if (not isinstance(senha, str) or len(senha) < 6 or re.search(r"\s", senha)
                or not re.search("[A-Z]", senha) or not re.search("[0-9]", senha)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha)):
                raise ErrorResponse(400, "A senha precisa de 6 caracteres, maiúscula, número e caractere especial.")

    def createService(self, dados):
        self.__validar_usuario(dados)
        nome = dados["nomeUsuario"].strip()
        email = dados["email"].strip().lower()
        if self.__usuarioDAO.findByEmail(email):
            raise ErrorResponse(400, "Já existe um usuário com este e-mail.")
        if self.__usuarioDAO.findByName(nome):
            raise ErrorResponse(400, "Já existe um usuário com este nome.")
        return self.__usuarioDAO.create(Usuario(nomeUsuario=nome, email=email, senha=dados["senha"]))

    def loginService(self, dados):
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        encontrado = self.__usuarioDAO.login(email.strip().lower(), senha)
        if not encontrado:
            raise ErrorResponse(401, "Usuário ou senha inválidos.")
        user = {
            "usuario": {
                "email": encontrado["email"],
                "name": encontrado["nomeUsuario"],
                "idUsuario": encontrado["idUsuario"]
            }
        }
        return {"user": user, "token": MeuTokenJWT().gerar_token(user["usuario"])}

    def findAllService(self):
        return self.__usuarioDAO.findAll()

    def findByIdService(self, idUsuario):
        usuario = self.__usuarioDAO.findById(idUsuario)
        if not usuario:
            raise ErrorResponse(404, "Usuário não encontrado.")
        return usuario

    def findPublicByIdService(self, idUsuario):
        usuario = self.findByIdService(idUsuario)
        return {"idUsuario": usuario["idUsuario"], "nomeUsuario": usuario["nomeUsuario"]}

    def updateService(self, idUsuario, dados, idAutenticado):
        if idUsuario != idAutenticado:
            raise ErrorResponse(403, "Você só pode alterar sua própria conta.")
        if not self.__usuarioDAO.findById(idUsuario):
            raise ErrorResponse(404, "Usuário não encontrado.")
        self.__validar_usuario(dados, exigir_senha=False)
        nome = dados["nomeUsuario"].strip()
        email = dados["email"].strip().lower()
        email_existente = self.__usuarioDAO.findByEmail(email)
        nome_existente = self.__usuarioDAO.findByName(nome)
        if email_existente and email_existente["idUsuario"] != idUsuario:
            raise ErrorResponse(400, "E-mail já cadastrado.")
        if nome_existente and nome_existente["idUsuario"] != idUsuario:
            raise ErrorResponse(400, "Nome de usuário já cadastrado.")
        return self.__usuarioDAO.update(Usuario(
            idUsuario=idUsuario, nomeUsuario=nome, email=email, senha=dados.get("senha")
        ))

    def deleteService(self, idUsuario, idAutenticado):
        if idUsuario != idAutenticado:
            raise ErrorResponse(403, "Você só pode excluir sua própria conta.")
        return self.__usuarioDAO.delete(idUsuario)
