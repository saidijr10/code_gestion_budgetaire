from django.db import models
from django.core.exceptions import ValidationError

class Prestataire(models.Model):
    TYPE_CHOICES = (
        ('physique', 'Personne Physique'),
        ('morale', 'Personne Morale'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Champs pour type physique
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    cin = models.CharField(max_length=20, blank=True, null=True, unique=True)

    # Champs pour type morale
    raison_sociale = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    # Champ commun
    tel = models.CharField(max_length=20)
    contact = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.type == 'physique':
            missing = []
            if not self.nom: missing.append('nom')
            if not self.prenom: missing.append('prenom')
            if not self.cin: missing.append('cin')
            if not self.tel: missing.append('tel')
            if missing:
                raise ValidationError({field: "Champ requis pour un prestataire physique." for field in missing})

        elif self.type == 'morale':
            missing = []
            if not self.raison_sociale: missing.append('raison_sociale')
            if not self.adresse: missing.append('adresse')
            if not self.tel: missing.append('tel')
            if not self.contact: missing.append('contact')
            if missing:
                raise ValidationError({field: "Champ requis pour un prestataire moral." for field in missing})

    def __str__(self):
        return self.nom or self.raison_sociale or "Prestataire"

class RIB(models.Model):
    rib = models.CharField(max_length=24, unique=True)
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE, related_name="ribs")

class Budget(models.Model):
    annee = models.IntegerField()
    type = models.CharField(max_length=20)
    date_creation = models.DateField()

from django.db.models import Sum

class LigneBudgetaire(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE)
    montant_budget_ttc = models.DecimalField(max_digits=10, decimal_places=2)
    rubrique = models.CharField(max_length=255, blank=True, null=True)
    sous_rubrique = models.CharField(max_length=255, blank=True, null=True)

    
    def montant_ordonnancement_total(self):
        return self.ordonnancement_set.aggregate(
            total=Sum('montant_ordonnancement')
        )['total'] or 0

    def montant_regle_total(self):
        return self.reglement_set.aggregate(
            total=Sum('montant_regler')
        )['total'] or 0

    def montant_disponible(self):
        total_ordonnancement = self.montant_ordonnancement_total()
        total_regle = self.montant_regle_total()
        return self.montant_budget_ttc - (total_ordonnancement - total_regle)
    @property
    def solde_affiche(self):
        return f"{self.montant_disponible():,.2f} MAD"

class Ordonnancement(models.Model):

    ligne = models.ForeignKey(LigneBudgetaire, on_delete=models.CASCADE)
    date_ordonnancement = models.DateField()
    montant_ordonnancement = models.DecimalField(max_digits=10, decimal_places=2)
    objet = models.CharField(max_length=255)
    justificatifs = models.TextField(blank=True, null=True)
  
    def clean(self):
        total_ordonnancement = self.ligne.ordonnancement_set.exclude(pk=self.pk).aggregate(
            total=models.Sum('montant_ordonnancement')
        )['total'] or 0

        total_reglement = self.ligne.reglement_set.aggregate(
            total=models.Sum('montant_regler')
        )['total'] or 0

        budget_ttc = self.ligne.montant_budget_ttc
        montant_total_apres = total_ordonnancement + self.montant_ordonnancement - total_reglement

        if montant_total_apres > budget_ttc:
            raise ValidationError(
                f"Le budget sera dépassé : {montant_total_apres} > {budget_ttc}. "
                f"Montant disponible réel : {budget_ttc - (total_ordonnancement - total_reglement)}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Appelle la validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ordonnancement {self.id} - {self.objet}"

    
class Reglement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
        ('espece', 'Espèce'),
    ]

    ligne = models.ForeignKey(LigneBudgetaire, on_delete=models.CASCADE)
    ordonnancement = models.ForeignKey(Ordonnancement, on_delete=models.CASCADE, null=True, blank=True)
    date_paiement = models.DateField()
    montant_regler = models.DecimalField(max_digits=10, decimal_places=2)
    justification = models.TextField(blank=True, null=True)
    compte_debite = models.CharField(max_length=50,blank=True, null=True)  # Compte à débiter saisi
    reglement_rel = models.CharField(max_length=50, blank=True, null=True)  # Référence du règlement
    ref_cheque = models.CharField(max_length=50, blank=True, null=True)  # Référence du chèque

    mode_paiement = models.CharField(
        max_length=10,
        choices=MODE_PAIEMENT_CHOICES,
        default='virement'
    )

    def __str__(self):
        return f"Règlement {self.id} - {self.ligne}"


class CodeBanque(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom_banque = models.CharField(max_length=255, blank=True, default="")
    def __str__(self):
        return self.code

class CodeLocalite(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code
    
