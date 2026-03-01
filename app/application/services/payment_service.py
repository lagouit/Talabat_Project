import uuid
from app.infrastructure.db.repositories.payment_repository import PaymentRepository

class PaymentService:
    def __init__(self):
        self.payment_repo = PaymentRepository()

    def effectuer_paiement_sequestre(self, commande_id):
        """Simule un paiement bancaire et bloque les fonds"""
        # Simulation d'un ID de transaction bancaire unique
        transaction_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        
        success = self.payment_repo.create_escrow(commande_id, transaction_id)
        if success:
            return True, f"Paiement sécurisé ! ID Transaction : {transaction_id}. Fonds bloqués par Talabat."
        return False, "Échec du paiement sécurisé."