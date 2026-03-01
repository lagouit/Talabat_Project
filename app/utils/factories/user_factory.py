from app.core.models.user import Beneficiaire, Fournisseur, Admin

class UserFactory:
    @staticmethod
    def create_user(data):
        """Transforme un dictionnaire (provenant de la BDD) en objet User POO"""
        if not data:
            return None
        
        role = data.get('role')
        # Paramètres communs
        params = {
            'id': data.get('id'),
            'nom': data.get('nom'),
            'email': data.get('email'),
            'telephone': data.get('telephone'),
            'adresse_livraison': data.get('adresse_livraison')
        }

        if role == 'beneficiaire':
            return Beneficiaire(**params)
        elif role == 'fournisseur':
            # Paramètres spécifiques au chef
            params['solde_accumule'] = data.get('solde_accumule', 0.0)
            params['kyc_valide'] = bool(data.get('kyc_valide', False))
            params['biographie'] = data.get('biographie', "")
            return Fournisseur(**params)
        elif role == 'admin':
            return Admin(**params)
        
        return None