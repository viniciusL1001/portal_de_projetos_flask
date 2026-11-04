import mysql.connector
from mysql.connector import pooling


class MysqlDatabase:
    def __init__(self, pool_name="pool_portal", pool_size=10,
                 host="127.0.0.1", user="root", password="",
                 database="portal_de_projetos", port=3306):
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.__pool = None

    def connect(self):
        if self.__pool is None:
            self.__pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name, pool_size=self.pool_size,
                host=self.host, user=self.user, password=self.password,
                database=self.database, port=self.port
            )
            connection = self.__pool.get_connection()
            connection.close()
            print("Conectado ao MySQL com sucesso.")
        return self.__pool

    def get_connection(self):
        return self.connect().get_connection()
