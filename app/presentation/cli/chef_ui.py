import os
from app.application.services.catalog_service import CatalogService
from app.application.services.order_service import OrderService


class ChefUI:
    def __init__(self, chef_user):
        self.chef = chef_user
        self.catalog_service = CatalogService()
        self.order_service = OrderService()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def gerer_commandes_recues(self):
        self.clear_screen()
        print("--- COMMANDES REÇUES ---")
        # On utilise le repository via le service (ou directement pour gagner du temps ici)
        commandes = self.order_service.order_repo.get_orders_by_chef(self.chef.id)
        
        if not commandes:
            input("Aucune commande reçue. Entrée...")
            return

        for c in commandes:
            print(f"ID: {c['id']} | Client: {c['client_nom']} | Total: {c['montant_total']} DH")
            print(f"STATUT ACTUEL : [{c['statut']}]")
            print("-" * 30)

        cid = input("\nID de la commande à gérer (0 pour retour) : ")
        if cid == "0": return

        print("\nNouveau statut :")
        print("1. ACCEPTER (Passer à ACCEPTE)")
        print("2. COMMENCER (Passer à EN_PREPARATION)")
        print("3. PRÊT (Passer à PRET)")
        
        choix = input("Votre choix : ")
        status_map = {"1": "ACCEPTE", "2": "EN_PREPARATION", "3": "PRET"}
        
        if choix in status_map:
            new_s = status_map[choix]
            success = self.order_service.order_repo.update_order_status(int(cid), new_s)
            if success:
                input(f"✅ Commande {cid} est maintenant : {new_s}. Entrée...")
            else:
                input("❌ Erreur lors du changement. Entrée...")

    def menu_principal(self):
        while True:
            self.clear_screen()
            print(f"=== ESPACE CHEF : {self.chef.nom} ===")
            print(f"Statut KYC : {'✅ Valide' if self.chef.kyc_valide else '❌ En attente'}")
            print("--------------------------------")
            print("1. Voir mes plats")
            print("2. Ajouter un nouveau plat")
            print("3. Gérer les commandes reçues")
            print("4. Déconnexion")
            
            choix = input("\nVotre choix : ")

            if choix == "1":
                self.afficher_mes_plats()
            elif choix == "2":
                self.formulaire_ajout_plat()
            elif choix == "3":
                self.gerer_commandes_recues()
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