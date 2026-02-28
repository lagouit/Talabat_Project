class Category:
    def _init_(self, id, libelle):
        self.id = id
        self.libelle = libelle

class Meal:
    def _init_(self, id=None, catalogue_id=None, categorie_id=None, titre="", prix=0.0, description="", est_disponible=True):
        self.id = id
        self.catalogue_id = catalogue_id
        self.categorie_id = categorie_id
        self.titre = titre
        self.prix = prix
        self.description = description
        self.est_disponible = est_disponible