from datetime import date
from api.model.usuario import Usuario
from api.model.projeto import Projeto
from api.model.comentario import Comentario
from api.utils.error_response import ErrorResponse


class ComentarioService:
    def __init__(self, comentario_dao, projeto_dao, usuario_dao):
        self.__comentarioDAO = comentario_dao
        self.__projetoDAO = projeto_dao
        self.__usuarioDAO = usuario_dao

    @staticmethod
    def __validar_nota_texto(dados):
        texto = dados.get("texto")
        nota = dados.get("nota")
        if not isinstance(texto, str) or not texto.strip() or len(texto) > 1000:
            raise ErrorResponse(400, "O texto do comentário é obrigatório (até 1000 caracteres).")
        if nota is not None and (type(nota) is not int or nota < 1 or nota > 5):
            raise ErrorResponse(400, "A nota deve estar entre 1 e 5.")

    def createService(self, dados, idAutenticado):
        self.__validar_nota_texto(dados)
        usuario = dados.get("usuario") or {}
        projeto = dados.get("projeto") or {}
        if usuario.get("idUsuario") != idAutenticado:
            raise ErrorResponse(403, "Você só pode comentar com sua própria conta.")
        id_projeto = projeto.get("idProjeto")
        if type(id_projeto) is not int or id_projeto <= 0:
            raise ErrorResponse(400, "idProjeto inválido.")
        if not self.__projetoDAO.findById(id_projeto):
            raise ErrorResponse(404, "Projeto não encontrado.")
        if not self.__usuarioDAO.findById(idAutenticado):
            raise ErrorResponse(404, "Usuário não encontrado.")
        comentario = Comentario(
            usuario=Usuario(idUsuario=idAutenticado),
            projeto=Projeto(idProjeto=id_projeto),
            nota=dados.get("nota"), texto=dados["texto"].strip(), dataComentario=date.today()
        )
        return self.__comentarioDAO.create(comentario)

    def updateService(self, idComentario, dados, idAutenticado):
        existente = self.findByIdService(idComentario)
        if existente["usuario"]["idUsuario"] != idAutenticado:
            raise ErrorResponse(403, "Somente o autor pode atualizar este comentário.")
        self.__validar_nota_texto(dados)
        comentario = Comentario(
            idComentario=idComentario,
            texto=dados["texto"].strip(),
            nota=existente["nota"] if "nota" not in dados else dados["nota"]
        )
        return self.__comentarioDAO.update(comentario, idAutenticado)

    def deleteService(self, idComentario, idAutenticado):
        existente = self.findByIdService(idComentario)
        if existente["usuario"]["idUsuario"] != idAutenticado:
            raise ErrorResponse(403, "Somente o autor pode excluir este comentário.")
        return self.__comentarioDAO.delete(idComentario, idAutenticado)

    def findAllService(self):
        return self.__comentarioDAO.findAll()

    def findByIdService(self, idComentario):
        comentario = self.__comentarioDAO.findById(idComentario)
        if not comentario:
            raise ErrorResponse(404, "Comentário não encontrado.")
        return comentario

    def findByIdProjetoService(self, idProjeto):
        if not self.__projetoDAO.findById(idProjeto):
            raise ErrorResponse(404, "Projeto não encontrado.")
        return self.__comentarioDAO.findByIdProjeto(idProjeto)
