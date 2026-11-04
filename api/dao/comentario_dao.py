from api.model.comentario import Comentario


class ComentarioDAO:
    def __init__(self, database):
        self.__database = database

    def create(self, comentario: Comentario):
        sql = ("INSERT INTO Comentario (idProjeto, idUsuario, nota, texto, dataComentario) "
               "VALUES (%s, %s, %s, %s, %s)")
        params = (comentario.projeto.idProjeto, comentario.usuario.idUsuario,
                  comentario.nota, comentario.texto, comentario.dataComentario)
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.lastrowid

    def update(self, comentario: Comentario, idUsuario):
        sql = ("UPDATE Comentario SET nota=%s, texto=%s "
               "WHERE idComentario=%s AND idUsuario=%s")
        params = (comentario.nota, comentario.texto, comentario.idComentario, idUsuario)
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idComentario, idUsuario):
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Comentario WHERE idComentario=%s AND idUsuario=%s",
                    (idComentario, idUsuario)
                )
                conn.commit()
                return cursor.rowcount > 0

    @staticmethod
    def __formatar(row):
        if not row:
            return None
        return {
            "idComentario": row["idComentario"],
            "nota": row["nota"],
            "texto": row["texto"],
            "dataComentario": row["dataComentario"].isoformat() if row["dataComentario"] else None,
            "usuario": {
                "idUsuario": row["idUsuario"],
                "nomeUsuario": row["nomeUsuario"]
            },
            "projeto": {
                "idProjeto": row["idProjeto"],
                "titulo": row["titulo"]
            }
        }

    def findAll(self):
        sql = ("SELECT Comentario.*, Usuario.nomeUsuario, Projeto.titulo "
               "FROM Comentario JOIN Usuario ON Comentario.idUsuario=Usuario.idUsuario "
               "JOIN Projeto ON Comentario.idProjeto=Projeto.idProjeto "
               "ORDER BY Comentario.idComentario")
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                return [self.__formatar(row) for row in cursor.fetchall()]

    def findById(self, idComentario):
        sql = ("SELECT Comentario.*, Usuario.nomeUsuario, Projeto.titulo "
               "FROM Comentario JOIN Usuario ON Comentario.idUsuario=Usuario.idUsuario "
               "JOIN Projeto ON Comentario.idProjeto=Projeto.idProjeto "
               "WHERE Comentario.idComentario=%s")
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (idComentario,))
                return self.__formatar(cursor.fetchone())

    def findByIdProjeto(self, idProjeto):
        sql = ("SELECT Comentario.*, Usuario.nomeUsuario FROM Comentario "
               "JOIN Usuario ON Comentario.idUsuario=Usuario.idUsuario "
               "WHERE Comentario.idProjeto=%s ORDER BY Comentario.idComentario")
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (idProjeto,))
                rows = cursor.fetchall()
        return [
            {
                "idComentario": row["idComentario"],
                "idProjeto": row["idProjeto"],
                "idUsuario": row["idUsuario"],
                "nomeUsuario": row["nomeUsuario"],
                "nota": row["nota"],
                "texto": row["texto"],
                "dataComentario": row["dataComentario"].isoformat() if row["dataComentario"] else None
            }
            for row in rows
        ]
