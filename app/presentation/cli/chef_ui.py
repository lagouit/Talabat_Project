import os
from app.application.services.catalog_service import CatalogService

class ChefUI:
    def __init__(self, chef_user):
        self.chef = chef_user
        self.catalog_service = CatalogService()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        while True:
            self.clear_screen()
            print(f"=== ESPACE CHEF : {self.chef.nom} ===")
            print(f"Statut KYC : {'✅ Valide' if self.chef.kyc_valide else '❌ En attente'}")
            print("--------------------------------")
            print("1. Voir mes plats")
            print("2. Ajouter un nouveau plat")
            print("3. Voir mes revenus (Bientôt)")
            print("4. Déconnexion")
            
            choix = input("\nVotre choix : ")

            if choix == "1":
                self.afficher_mes_plats()
            elif choix == "2":
                self.formulaire_ajout_plat()
            elif choix == "4":
                break

    def afficher_mes_plats(self):
        self.clear_screen()
        print("--- MES PLATS AU CATALOGUE ---")
        plats = self.catalog_service.lister_mes_plats(self.chef.id)
        
        if not plats:
            print("Vous n'avez aucun plat pour le moment.")
        else:
            for p in plats:
                print(f"[{p['id']}] {p['titre']} - {p['prix']} DH")
                print(f"    Description : {p['description']}")
        
        input("\nAppuyez sur Entrée pour revenir...")

    def formulaire_ajout_plat(self):
        self.clear_screen()
        print("--- AJOUTER UN NOUVEAU PLAT ---")
        
        # 1. Sélection de la catégorie
        categories = self.catalog_service.obtenir_categories()
        print("\nCatégories disponibles :")
        for cat in categories:
            print(f"{cat['id']}. {cat['libelle']}")
        
        cat_id = input("\nID de la catégorie : ")
        titre = input("Nom du plat : ")
        
        try:
            prix = float(input("Prix (DH) : "))
        except ValueError:
            print("Prix invalide !")
            input()
            return

        desc = input("Description : ")

        success, msg = self.catalog_service.ajouter_plat(self.chef.id, cat_id, titre, prix, desc)
        input(f"\n{msg} Appuyez sur Entrée...")
        input(f"\n{msg} Appuyez sur Entrée...")