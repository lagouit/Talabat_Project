import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host='localhost',
                    user='root',       # À vérifier selon ton XAMPP
                    password='Lagouit123@',       # À vérifier
                    database='talabat_db'
                )
            except Error as e:
                print(f"Erreur de connexion MySQL: {e}")
        return self._connection

    def get_cursor(self):
        conn = self.connect()
        if conn:
            return conn.cursor(dictionary=True) # Retourne les résultats en dict {'id': 1, 'nom': '...'}
        return None

    def commit(self):
        if self._connection:
            self._connection.commit()