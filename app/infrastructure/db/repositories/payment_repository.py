from app.infrastructure.db.database_manager import DatabaseManager

class PaymentRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def create_escrow(self, commande_id, transaction_id):
        """Crée l'enregistrement du blocage des fonds"""
        cursor = self.db.get_cursor()
        query = """
            INSERT INTO paiements_sequestre (commande_id, transaction_id, est_bloque)
            VALUES (%s, %s, 1)
        """
        try:
            cursor.execute(query, (commande_id, transaction_id))
            # On met aussi à jour le statut de la commande
            cursor.execute("UPDATE commandes SET statut = 'PAYE_SEQUESTRE' WHERE id = %s", (commande_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Erreur Paiement SQL: {e}")
            return False