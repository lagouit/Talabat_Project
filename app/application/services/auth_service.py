from app.infrastructure.db.repositories.user_repository import UserRepository
from app.utils.factories.user_factory import UserFactory

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def login(self, email, password):
        """Vérifie les identifiants et retourne un objet User"""
        user_data = self.user_repo.find_by_email(email)
        
        # Comparaison simple (En production, on utiliserait du hachage comme bcrypt)
        if user_data and user_data['mot_de_passe'] == password:
            # Transformation du dictionnaire SQL en objet POO
            return UserFactory.create_user(user_data)
        
        return None

    def register(self, nom, email, password, role, telephone=""):
        """Gère l'inscription d'un nouvel utilisateur"""
        if self.user_repo.find_by_email(email):
            return False, "Cet email est déjà utilisé."
        
        user_id = self.user_repo.save(nom, email, password, role, telephone)
        if user_id:
            return True, "Inscription réussie !"
        return False, "Une erreur est survenue lors de l'enregistrement."