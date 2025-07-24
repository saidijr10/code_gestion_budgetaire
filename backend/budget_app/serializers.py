from rest_framework import serializers
from .models import Prestataire
from .models import RIB
from .models import Budget
from .models import LigneBudgetaire
from .models import Ordonnancement
from .models import Reglement
from .models import CodeBanque, CodeLocalite


class PrestataireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestataire
        fields = '__all__'

    def validate(self, data):
        # Crée une instance temporaire pour appeler clean()
        instance = Prestataire(**data)
        instance.clean()
        return data
    

class RIBSerializer(serializers.ModelSerializer):
    prestataire_info = PrestataireSerializer(source='prestataire', read_only=True)

    class Meta:
        model = RIB
        fields = ['id', 'rib', 'prestataire', 'prestataire_info']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

from rest_framework import serializers
from .models import LigneBudgetaire, Budget, Prestataire
from .serializers import BudgetSerializer, PrestataireSerializer
from django.db.models import Sum

class LigneBudgetaireSerializer(serializers.ModelSerializer):
    budget = BudgetSerializer(read_only=True)
    prestataire = PrestataireSerializer(read_only=True)
    total_ordonnancement = serializers.SerializerMethodField()
    total_reglement = serializers.SerializerMethodField()
    budget_id = serializers.PrimaryKeyRelatedField(
        queryset=Budget.objects.all(), source='budget', write_only=True
    )
    prestataire_id = serializers.PrimaryKeyRelatedField(
        queryset=Prestataire.objects.all(), source='prestataire', write_only=True
    )
    rib = serializers.SerializerMethodField()
 
    domiciliation = serializers.SerializerMethodField()  

    class Meta:
        model = LigneBudgetaire
        fields = [
            'id',
            'budget',
            'prestataire',
            'montant_budget_ttc',
            'budget_id',
            'prestataire_id',
            'rib',
            'domiciliation',   
            'total_ordonnancement',
            'total_reglement',
            'rubrique',           
            'sous_rubrique'    
        ]

    def get_rib(self, obj):
        prestataire = obj.prestataire
        rib_obj = prestataire.ribs.last()
        return rib_obj.rib if rib_obj else None

    def get_total_ordonnancement(self, obj):
        return obj.ordonnancement_set.aggregate(total=Sum('montant_ordonnancement'))['total'] or 0

    def get_total_reglement(self, obj):
        return obj.reglement_set.aggregate(total=Sum('montant_regler'))['total'] or 0

    def get_domiciliation(self, obj):
        prestataire = obj.prestataire
        rib_obj = prestataire.ribs.last()
        rib = rib_obj.rib if rib_obj else None

        if not rib:
            return ""

        code_banque = rib[:3]  # 3 premiers caractères
        banque = CodeBanque.objects.filter(code=code_banque).first()
        return banque.nom_banque if banque else ""


class OrdonnancementSerializer(serializers.ModelSerializer):
    budget = serializers.SerializerMethodField()
    prestataire = serializers.SerializerMethodField()
    rib = serializers.SerializerMethodField()
    

    class Meta:
        model = Ordonnancement
        fields = [
            'id',
            'ligne',
            'objet',
            'date_ordonnancement',
            'montant_ordonnancement',
            'justificatifs',
            'budget',
            'prestataire',
            'rib',
        ]

    def get_budget(self, obj):
        return {
            'id': obj.ligne.budget.id,
            'annee': obj.ligne.budget.annee,
            'type': obj.ligne.budget.type
        }

    def get_prestataire(self, obj):
        p = obj.ligne.prestataire
        return {
            'id': p.id,
            'type': p.type,
            'nom': p.nom,
            'prenom': p.prenom,
            'raison_sociale': p.raison_sociale,
            'adresse': p.adresse,
            'tel': p.tel,
            'contact': p.contact,
        }

    def get_rib(self, obj):
        prestataire = obj.ligne.prestataire
        rib_obj = prestataire.ribs.first()
        return rib_obj.rib if rib_obj else None

class ReglementSerializer(serializers.ModelSerializer):
    ligne = LigneBudgetaireSerializer(read_only=True)
    ligne_id = serializers.PrimaryKeyRelatedField(
    queryset=LigneBudgetaire.objects.all(),
    source='ligne',
    write_only=True
)

    

    class Meta:
        model = Reglement
        fields = [
            'id', 'ligne', 'ligne_id', 'date_paiement', 'montant_regler',
            'justification', 'compte_debite','ref_cheque','mode_paiement','reglement_rel'
        ]

    def get_prestataire(self, obj):
        p = obj.ligne.prestataire if obj.ligne else None
        if not p:
            return None
        return {
            'id': p.id,
            'type': p.type,
            'nom': p.nom,
            'prenom': p.prenom,
            'raison_sociale': p.raison_sociale,
            'adresse': p.adresse,
            'tel': p.tel,
            'contact': p.contact,
        }
    

    def get_rib(self, obj):
        p = obj.ligne.prestataire if obj.ligne else None
        if not p:
            return None
        rib_obj = p.ribs.first()
        return rib_obj.rib if rib_obj else None



class CodeBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBanque
        fields = ['id', 'code','nom_banque']  # adapte si tu as plus de champs

class CodeLocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeLocalite
        fields = ['id', 'code']