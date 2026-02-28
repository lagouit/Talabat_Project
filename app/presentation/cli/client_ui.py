import os
from app.application.services.catalog_service import CatalogService

class ClientUI:
    def _init_(self, client_user):
        self.client = client_user
        self.catalog_service = CatalogService()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        while True:
            self.clear_screen()
            print(f"=== ESPACE CLIENT : {self.client.nom} ===")
            print("--------------------------------")
            print("1. Parcourir tous les repas")
            print("2. Filtrer par catégorie")
            print("3. Filtrer par prix maximum")
            print("4. Déconnexion")
            
            choix = input("\nVotre choix : ")

            if choix == "1":
                self.afficher_repas()
            elif choix == "2":
                self.filtrer_par_categorie()
            elif choix == "3":
                self.filtrer_par_prix()
            elif choix == "4":
                break

    def afficher_repas(self, cat_id=None, p_max=None):
        self.clear_screen()
        print("--- REPAS DISPONIBLES ---")
        repas = self.catalog_service.rechercher_repas(cat_id, p_max)
        
        if not repas:
            print("Aucun repas ne correspond à votre recherche.")
        else:
            for r in repas:
                print(f"[{r['id']}] {r['titre']} | {r['prix']} DH | Chef: {r['chef_nom']}")
                print(f"    Catégorie: {r['categorie_nom']} | Description: {r['description']}")
                print("-" * 30)
        
        input("\nAppuyez sur Entrée pour continuer...")

    def filtrer_par_categorie(self):
        cats = self.catalog_service.obtenir_categories()
        print("\nChoisissez une catégorie :")
        for c in cats:
            print(f"{c['id']}. {c['libelle']}")
        cid = input("ID : ")
        self.afficher_repas(cat_id=cid)

    def filtrer_par_prix(self):
        pmax = input("\nPrix maximum (DH) : ")
        try:
            self.afficher_repas(p_max=float(pmax))
        except ValueError:
            input("Prix invalide.")