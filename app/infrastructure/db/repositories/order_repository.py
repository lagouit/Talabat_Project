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
    
    def get_orders_by_chef(self, chef_id):
        """Récupère les commandes destinées à ce chef (avec détails client)"""
        cursor = self.db.get_cursor()
        query = """
            SELECT c.*, u.nom as client_nom, u.telephone as client_tel
            FROM commandes c
            JOIN utilisateurs u ON c.beneficiaire_id = u.id
            WHERE c.fournisseur_id = %s
            ORDER BY c.date_commande DESC
        """
        cursor.execute(query, (chef_id,))
        return cursor.fetchall()

    def update_order_status(self, order_id, new_status):
        """Met à jour le statut et historise le changement"""
        cursor = self.db.get_cursor()
        try:
            # 1. Récupérer l'ancien statut pour l'historique
            cursor.execute("SELECT statut FROM commandes WHERE id = %s", (order_id,))
            old_status = cursor.fetchone()['statut']

            # 2. Mise à jour du statut principal
            cursor.execute("UPDATE commandes SET statut = %s WHERE id = %s", (new_status, order_id))

            # 3. Insertion dans l'historique (Traçabilité SQL)
            query_hist = """
                INSERT INTO historique_statuts (commande_id, ancien_statut, nouveau_statut)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_hist, (order_id, old_status, new_status))
            
            self.db.commit()
            return True
        except Exception as e:
            print(f"Erreur Update Status: {e}")
            return False