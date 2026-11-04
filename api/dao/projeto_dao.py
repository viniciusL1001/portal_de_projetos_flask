from datetime import date
from api.model.projeto import Projeto


class ProjetoDAO:
    def __init__(self, database):
        self.__database = database

    def create(self, projeto: Projeto):
        sql = ("INSERT INTO Projeto (idUsuario, titulo, descricao, dataCriacao, imagem, linkGitHub) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        params = (projeto.usuario.idUsuario, projeto.titulo, projeto.descricao,
                  projeto.dataCriacao, projeto.imagem, projeto.linkGitHub)
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.lastrowid

    def update(self, projeto: Projeto):
        sql = ("UPDATE Projeto SET titulo=%s, descricao=%s, imagem=%s, linkGitHub=%s "
               "WHERE idProjeto=%s AND idUsuario=%s")
        params = (projeto.titulo, projeto.descricao, projeto.imagem, projeto.linkGitHub,
                  projeto.idProjeto, projeto.usuario.idUsuario)
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idProjeto, idUsuario):
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Projeto WHERE idProjeto=%s AND idUsuario=%s",
                    (idProjeto, idUsuario)
                )
                conn.commit()
                return cursor.rowcount > 0

    @staticmethod
    def __formatar(row):
        if not row:
            return None
        return {
            "idProjeto": row["idProjeto"],
            "titulo": row["titulo"],
            "descricao": row["descricao"],
            "dataCriacao": row["dataCriacao"].isoformat() if row["dataCriacao"] else None,
            "imagem": row["imagem"],
            "linkGitHub": row["linkGitHub"],
            "usuario": {
                "idUsuario": row["idUsuario"],
                "nomeUsuario": row["nomeUsuario"]
            }
        }

    def findAll(self):
        sql = ("SELECT Projeto.*, Usuario.nomeUsuario FROM Projeto "
               "JOIN Usuario ON Projeto.idUsuario=Usuario.idUsuario "
               "ORDER BY Projeto.idProjeto")
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                return [self.__formatar(row) for row in cursor.fetchall()]

    def findById(self, idProjeto):
        sql = ("SELECT Projeto.*, Usuario.nomeUsuario FROM Projeto "
               "JOIN Usuario ON Projeto.idUsuario=Usuario.idUsuario "
               "WHERE Projeto.idProjeto=%s")
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (idProjeto,))
                return self.__formatar(cursor.fetchone())
