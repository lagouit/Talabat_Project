import os
from app.application.services.catalog_service import CatalogService
from app.core.models.order import Order, OrderLine
from app.application.services.order_service import OrderService
from app.application.services.payment_service import PaymentService

class ClientUI:
    def __init__(self, client_user):
        self.client = client_user
        self.catalog_service = CatalogService()
        self.order_service = OrderService()
        self.panier = None # Contiendra l'objet Order en cours
        self.payment_service = PaymentService()

    def ajouter_au_panier(self, meal_id):
        """Ajoute un plat au panier en mémoire"""
        # 1. On récupère les détails du plat via le service
        # Pour simplifier, on recherche le plat dans la liste globale
        repas_liste = self.catalog_service.rechercher_repas()
        plat_choisi = next((r for r in repas_liste if r['id'] == int(meal_id)), None)

        if not plat_choisi:
            input("Plat introuvable. Entrée...")
            return

        try:
            qte = int(input(f"Quantité pour '{plat_choisi['titre']}' : "))
        except ValueError:
            input("Quantité invalide. Entrée...")
            return

        # 2. Initialiser la commande si c'est le premier article
        if self.panier is None:
            self.panier = Order(beneficiaire_id=self.client.id, fournisseur_id=plat_choisi['fournisseur_id'])
        
        # 3. Vérifier que c'est le même chef (règle métier : 1 commande = 1 chef)
        if self.panier.fournisseur_id != plat_choisi['fournisseur_id']:
            input("Erreur : Vous ne pouvez commander chez deux chefs différents en même temps. Videz votre panier d'abord.")
            return

        # 4. Ajouter la ligne
        ligne = OrderLine(plat_choisi['id'], plat_choisi['titre'], plat_choisi['prix'], qte)
        self.panier.lignes.append(ligne)
        input(f"Produit ajouté ! Total actuel : {self.panier.calculer_total()} DH. Entrée...")

    def voir_panier_et_valider(self):
        """Affiche le récapitulatif et enregistre en BDD"""
        self.clear_screen()
        if not self.panier or not self.panier.lignes:
            input("Votre panier est vide. Appuyez sur Entrée...")
            return

        print("--- VOTRE PANIER ---")
        for l in self.panier.lignes:
            print(f"- {l.titre} x{l.quantite} : {l.prix_unitaire * l.quantite} DH")
        
        total = self.panier.calculer_total()
        print(f"\nTOTAL À PAYER : {total} DH")
        print("--------------------")
        
        confirm = input("Valider la commande ? (o/n) : ")
        if confirm.lower() == 'o':
            success, msg = self.order_service.valider_commande(self.panier)
            if success:
                self.panier = None # On vide le panier après succès
            input(f"\n{msg} Appuyez sur Entrée...")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def gerer_paiements(self):
        self.clear_screen()
        print("COMMANDES EN ATTENTE DE PAIEMENT")
        # Ici on simplifie en récupérant la commande qu'on vient juste de créer
        # Dans un vrai projet, on listerait les commandes avec statut 'ATTENTE_PAIEMENT'
        
        cmd_id = input("\nEntrez l'ID de la commande à payer (ou 0 pour retour) : ")
        if cmd_id == "0": return

        print(f"\nConnexion à la passerelle de paiement sécurisée...")
        success, msg = self.payment_service.effectuer_paiement_sequestre(int(cmd_id))
        
        if success:
            print("✅ ARGENT BLOQUÉ EN SÉQUESTRE")
            input(f"{msg}\nAppuyez sur Entrée")
        else:
            input(f"{msg}\nAppuyez sur Entrée")

    def menu_principal(self):
        while True:
            self.clear_screen()
            print(f"=== ESPACE CLIENT : {self.client.nom} ===")
            print("--------------------------------")
            print("1. Parcourir tous les repas")
            print("2. Filtrer par catégorie")
            print("3. Filtrer par prix maximum")
            print("4. Déconnexion")
            print("5. Mes commandes à payer")

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