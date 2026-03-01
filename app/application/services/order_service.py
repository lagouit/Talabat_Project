from app.infrastructure.db.repositories.order_repository import OrderRepository

class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()

    def valider_commande(self, order_obj):
        """Vérifie si le panier est valide et l'enregistre en BDD"""
        if not order_obj.lignes:
            return False, "Le panier est vide."
        
        order_id = self.order_repo.save_order(order_obj)
        if order_id:
            return True, f"Commande n°{order_id} enregistrée. En attente de paiement."
        return False, "Erreur lors de la validation."