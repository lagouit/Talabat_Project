from app.infrastructure.db.repositories.meal_repository import MealRepository

class CatalogService:
    def __init__(self):
        self.meal_repo = MealRepository()

    def obtenir_categories(self):
        """Récupère la liste des catégories pour l'affichage dans le menu"""
        return self.meal_repo.get_all_categories()

    def ajouter_plat(self, chef_id, categorie_id, titre, prix, description):
        """Logique métier pour ajouter un plat au catalogue d'un chef spécifique"""
        try:
            # 1. On s'assure que le chef possède bien un catalogue dans la BDD
            catalogue_id = self.meal_repo.create_catalogue_if_not_exists(chef_id)
            
            # 2. On insère le repas lié à ce catalogue
            new_id = self.meal_repo.add_meal(
                catalogue_id, 
                categorie_id, 
                titre, 
                prix, 
                description
            )
            return True, f"Plat '{titre}' ajouté avec succès (ID: {new_id})."
        except Exception as e:
            return False, f"Erreur lors de l'ajout : {str(e)}"

    def lister_mes_plats(self, chef_id):
        """Récupère tous les plats appartenant à un chef"""
        return self.meal_repo.get_meals_by_chef(chef_id)
        
        
    def rechercher_repas(self, category_id=None, price_max=None):
        return self.meal_repo.get_available_meals(category_id, price_max)