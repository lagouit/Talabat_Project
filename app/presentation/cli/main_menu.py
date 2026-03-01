import os
from app.application.services.auth_service import AuthService
from app.presentation.cli.chef_ui import ChefUI
from app.presentation.cli.client_ui import ClientUI  # <-- Nouvel import

class MainMenu:
    def __init__(self):
        self.auth_service = AuthService()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher_accueil(self):
        while True:
            self.clear_screen()
            print("=== BIENVENUE SUR TALABAT ===")
            print("1. Se connecter")
            print("2. S'inscrire")
            print("3. Quitter")
            
            choix = input("\nVotre choix : ")

            if choix == "1":
                self.menu_connexion()
            elif choix == "2":
                self.menu_inscription()
            elif choix == "3":
                print("Au revoir !")
                break

    def menu_connexion(self):
        self.clear_screen()
        print("--- CONNEXION ---")
        email = input("Email : ")
        password = input("Mot de passe : ")
        
        user = self.auth_service.login(email, password)
        
        if user:
            # REDIRECTION SELON LE RÔLE
            if user.role == "fournisseur":
                interface_chef = ChefUI(user)
                interface_chef.menu_principal()
            elif user.role == "beneficiaire":
                interface_client = ClientUI(user) # <-- Liaison activée
                interface_client.menu_principal()
        else:
            input("\nEmail ou mot de passe incorrect. Appuyez sur Entrée...")

    def menu_inscription(self):
        self.clear_screen()
        print("--- INSCRIPTION ---")
        nom = input("Nom complet : ")
        email = input("Email : ")
        password = input("Mot de passe : ")
        print("Roles : 1. Bénéficiaire | 2. Fournisseur (Chef)")
        role_choix = input("Choix du rôle : ")
        role = "beneficiaire" if role_choix == "1" else "fournisseur"
        tel = input("Téléphone : ")

        success, message = self.auth_service.register(nom, email, password, role, tel)
        input(f"\n{message} Appuyez sur Entrée...")