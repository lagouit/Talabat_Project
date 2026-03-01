class EscrowPayment:
    def __init__(self, id=None, commande_id=None, transaction_id="", est_bloque=True):
        self.id = id
        self.commande_id = commande_id
        self.transaction_id = transaction_id
        self.est_bloque = est_bloque

    def liberer_fonds(self):
        self.est_bloque = False