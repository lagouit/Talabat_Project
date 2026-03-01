class User:
    def __init__(self, id=None, nom="", email="", role="", telephone="", adresse_livraison=""):
        self.id = id
        self.nom = nom
        self.email = email
        self.role = role
        self.telephone = telephone
        self.adresse_livraison = adresse_livraison

class Beneficiaire(User):
    def __init__(self, **kwargs):
        super().__init__(role="beneficiaire", **kwargs)

class Fournisseur(User):
    def __init__(self, solde_accumule=0.0, kyc_valide=False, biographie="", **kwargs):
        super().__init__(role="fournisseur", **kwargs)
        self.solde_accumule = solde_accumule
        self.kyc_valide = kyc_valide
        self.biographie = biographie

class Admin(User):
    def __init__(self, **kwargs):
        super().__init__(role="admin", **kwargs)