class OrderLine:
    def __init__(self, meal_id, titre, prix_unitaire, quantite):
        self.meal_id = meal_id
        self.titre = titre
        self.prix_unitaire = prix_unitaire
        self.quantite = quantite

class Order:
    def __init__(self, id=None, beneficiaire_id=None, fournisseur_id=None, statut="ATTENTE_PAIEMENT"):
        self.id = id
        self.beneficiaire_id = beneficiaire_id
        self.fournisseur_id = fournisseur_id
        self.statut = statut
        self.lignes = [] # Liste d'objets OrderLine

    def calculer_total(self):
        return sum(ligne.prix_unitaire * ligne.quantite for ligne in self.lignes)