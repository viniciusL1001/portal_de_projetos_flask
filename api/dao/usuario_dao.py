import bcrypt
from api.model.usuario import Usuario


class UsuarioDAO:
    def __init__(self, database):
        self.__database = database

    def create(self, usuario: Usuario):
        hash_senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")
        sql = "INSERT INTO Usuario (nomeUsuario, email, senha) VALUES (%s, %s, %s)"
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (usuario.nomeUsuario, usuario.email, hash_senha))
                conn.commit()
                return cursor.lastrowid

    def update(self, usuario: Usuario):
        sql = "UPDATE Usuario SET nomeUsuario=%s, email=%s"
        params = [usuario.nomeUsuario, usuario.email]
        if usuario.senha:
            sql += ", senha=%s"
            params.append(bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8"))
        sql += " WHERE idUsuario=%s"
        params.append(usuario.idUsuario)
        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idUsuario):
        # Exclui dependências antes da conta, numa transação.
        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "DELETE FROM Comentario WHERE idUsuario=%s OR idProjeto IN "
                    "(SELECT idProjeto FROM Projeto WHERE idUsuario=%s)",
                    (idUsuario, idUsuario)
                )
                cursor.execute("DELETE FROM Projeto WHERE idUsuario=%s", (idUsuario,))
                cursor.execute("DELETE FROM Usuario WHERE idUsuario=%s", (idUsuario,))
                excluiu = cursor.rowcount > 0
                conn.commit()
                return excluiu
            finally:
                cursor.close()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def findAll(self):
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idUsuario, nomeUsuario FROM Usuario ORDER BY idUsuario")
                return cursor.fetchall()

    def findById(self, idUsuario):
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT idUsuario, nomeUsuario, email FROM Usuario WHERE idUsuario=%s",
                    (idUsuario,)
                )
                return cursor.fetchone()

    def findByEmail(self, email):
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idUsuario FROM Usuario WHERE email=%s", (email,))
                return cursor.fetchone()

    def findByName(self, nomeUsuario):
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT idUsuario FROM Usuario WHERE nomeUsuario=%s", (nomeUsuario,))
                return cursor.fetchone()

    def login(self, email, senha):
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Usuario WHERE email=%s", (email,))
                usuario = cursor.fetchone()
        if not usuario:
            return None
        if not bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
            return None
        return {
            "idUsuario": usuario["idUsuario"],
            "nomeUsuario": usuario["nomeUsuario"],
            "email": usuario["email"]
        }
