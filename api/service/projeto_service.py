from datetime import date
from api.model.usuario import Usuario
from api.model.projeto import Projeto
from api.utils.error_response import ErrorResponse


class ProjetoService:
    def __init__(self, projeto_dao, usuario_dao):
        self.__projetoDAO = projeto_dao
        self.__usuarioDAO = usuario_dao

    def __validar(self, dados, idAutenticado):
        usuario = dados.get("usuario") or {}
        if usuario.get("idUsuario") != idAutenticado:
            raise ErrorResponse(403, "Você só pode publicar projetos na própria conta.")
        titulo = dados.get("titulo")
        link = dados.get("linkGitHub")
        if not isinstance(titulo, str) or not titulo.strip() or len(titulo) > 100:
            raise ErrorResponse(400, "Título do projeto inválido.")
        if not isinstance(link, str) or not link.strip().lower().startswith(("https://github.com/", "https://www.github.com/")):
            raise ErrorResponse(400, "Informe um link válido do GitHub.")
        if not self.__usuarioDAO.findById(idAutenticado):
            raise ErrorResponse(404, "Usuário não encontrado.")

    def createService(self, dados, idAutenticado):
        self.__validar(dados, idAutenticado)
        projeto = Projeto(
            usuario=Usuario(idUsuario=idAutenticado),
            titulo=dados["titulo"].strip(),
            descricao=dados.get("descricao"),
            imagem=dados.get("imagem"),
            linkGitHub=dados["linkGitHub"].strip(),
            dataCriacao=date.today()
        )
        projeto.idProjeto = self.__projetoDAO.create(projeto)
        return {
            "idProjeto": projeto.idProjeto,
            "titulo": projeto.titulo,
            "descricao": projeto.descricao,
            "imagem": projeto.imagem,
            "linkGitHub": projeto.linkGitHub,
            "usuario": {"idUsuario": idAutenticado}
        }

    def updateService(self, idProjeto, dados, idAutenticado):
        existente = self.findByIdService(idProjeto)
        if existente["usuario"]["idUsuario"] != idAutenticado:
            raise ErrorResponse(403, "Somente o autor pode atualizar este projeto.")
        self.__validar(dados, idAutenticado)
        projeto = Projeto(
            idProjeto=idProjeto, usuario=Usuario(idUsuario=idAutenticado),
            titulo=dados["titulo"].strip(), descricao=dados.get("descricao"),
            imagem=dados.get("imagem"), linkGitHub=dados["linkGitHub"].strip()
        )
        return self.__projetoDAO.update(projeto)

    def deleteService(self, idProjeto, idAutenticado):
        existente = self.findByIdService(idProjeto)
        if existente["usuario"]["idUsuario"] != idAutenticado:
            raise ErrorResponse(403, "Somente o autor pode excluir este projeto.")
        return self.__projetoDAO.delete(idProjeto, idAutenticado)

    def findAllService(self):
        return self.__projetoDAO.findAll()

    def findByIdService(self, idProjeto):
        projeto = self.__projetoDAO.findById(idProjeto)
        if not projeto:
            raise ErrorResponse(404, "Projeto não encontrado.")
        return projeto
