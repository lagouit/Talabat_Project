# Ajoute cet import en haut du fichier
from app.presentation.cli.chef_ui import ChefUI

# Modifie la fin de la méthode menu_connexion :
    def menu_connexion(self):
        # ... (code existant pour email/password et login)
        user = self.auth_service.login(email, password)
        if user:
            print(f"\nSuccès ! Bienvenue {user.nom}.")
            if user.role == "fournisseur":
                chef_app = ChefUI(user)
                chef_app.menu_principal()
            elif user.role == "beneficiaire":
                print("Espace Bénéficiaire à venir...")
                input()
        else:
            input("\nEmail ou mot de passe incorrect. Appuyez sur Entrée...")