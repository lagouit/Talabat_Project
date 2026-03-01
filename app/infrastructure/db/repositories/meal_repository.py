from app.infrastructure.db.database_manager import DatabaseManager

class MealRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_categories(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM categories")
        return cursor.fetchall()

    def create_catalogue_if_not_exists(self, chef_id):
        """Vérifie si le chef a un catalogue, sinon le crée"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id FROM catalogues WHERE fournisseur_id = %s", (chef_id,))
        cat = cursor.fetchone()
        if not cat:
            cursor.execute("INSERT INTO catalogues (fournisseur_id, nom_menu) VALUES (%s, %s)", 
                           (chef_id, f"Menu de Chef {chef_id}"))
            self.db.commit()
            return cursor.lastrowid
        return cat['id']

    def add_meal(self, catalogue_id, categorie_id, titre, prix, description):
        cursor = self.db.get_cursor()
        query = """
            INSERT INTO repas (catalogue_id, categorie_id, titre, prix, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (catalogue_id, categorie_id, titre, prix, description))
        self.db.commit()
        return cursor.lastrowid

    def get_meals_by_chef(self, chef_id):
        cursor = self.db.get_cursor()
        query = """
            SELECT r.* FROM repas r 
            JOIN catalogues c ON r.catalogue_id = c.id 
            WHERE c.fournisseur_id = %s
        """
        cursor.execute(query, (chef_id,))
        return cursor.fetchall()
        
    def get_available_meals(self, category_id=None, price_max=None):
        """Récupère les repas filtrés avec le nom du chef"""
        cursor = self.db.get_cursor()
        query = """
            SELECT r.*, u.nom as chef_nom, cat.libelle as categorie_nom 
            FROM repas r
            JOIN catalogues c ON r.catalogue_id = c.id
            JOIN utilisateurs u ON c.fournisseur_id = u.id
            JOIN categories cat ON r.categorie_id = cat.id
            WHERE r.est_disponible = 1
        """
        params = []
        if category_id:
            query += " AND r.categorie_id = %s"
            params.append(category_id)
        if price_max:
            query += " AND r.prix <= %s"
            params.append(price_max)
            
        cursor.execute(query, tuple(params))
        return cursor.fetchall()