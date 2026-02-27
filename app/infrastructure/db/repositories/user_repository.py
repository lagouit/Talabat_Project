from app.infrastructure.db.database_manager import DatabaseManager

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def find_by_email(self, email):
        """Recherche un utilisateur par email (pour la connexion)"""
        cursor = self.db.get_cursor()
        query = "SELECT * FROM utilisateurs WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def save(self, nom, email, mot_de_passe, role, telephone=""):
        """Enregistre un nouvel utilisateur"""
        cursor = self.db.get_cursor()
        query = """
            INSERT INTO utilisateurs (nom, email, mot_de_passe, role, telephone)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (nom, email, mot_de_passe, role, telephone))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return None
        finally:
            cursor.close()