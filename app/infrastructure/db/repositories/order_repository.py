from app.infrastructure.db.database_manager import DatabaseManager

class OrderRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def save_order(self, order_obj):
        """Enregistre la commande et ses lignes (Transaction SQL)"""
        cursor = self.db.get_cursor()
        try:
            # 1. Insertion dans la table commandes
            query_order = """
                INSERT INTO commandes (beneficiaire_id, fournisseur_id, montant_total, statut)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_order, (
                order_obj.beneficiaire_id, 
                order_obj.fournisseur_id, 
                order_obj.calculer_total(), 
                order_obj.statut
            ))
            order_id = cursor.lastrowid

            # 2. Insertion des lignes de commande
            query_line = """
                INSERT INTO lignes_commande (commande_id, repas_id, quantite, prix_unitaire_achat)
                VALUES (%s, %s, %s, %s)
            """
            for ligne in order_obj.lignes:
                cursor.execute(query_line, (order_id, ligne.meal_id, ligne.quantite, ligne.prix_unitaire))

            self.db.commit()
            return order_id
        except Exception as e:
            print(f"Erreur SQL Order: {e}")
            return None
        finally:
            cursor.close()