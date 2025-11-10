from django.core.management.base import BaseCommand
from budget_app.models import CodeBanque
import pandas as pd
import os

class Command(BaseCommand):
    help = "Met à jour les noms des banques depuis un fichier Excel"

    def handle(self, *args, **kwargs):
        # Chemin vers le fichier Excel
        file_path = os.path.join(os.path.dirname(__file__), 'domicialisation.xlsx')
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"⚠️ Fichier introuvable : {file_path}"))
            return

        try:
            df = pd.read_excel(file_path)
            df.columns = df.columns.str.strip()  # Nettoyer les colonnes
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lecture Excel : {e}"))
            return

        updated = 0
        not_found = []
        for _, row in df.iterrows():
            code = row.get('Code Banque')
            nom_banque = row.get('Nom_Banque')

            if pd.isna(code) or pd.isna(nom_banque):
                continue

            code_str = str(code).strip().zfill(3)  # Toujours 3 chiffres
            nom_banque_str = str(nom_banque).strip()

            try:
                banque = CodeBanque.objects.get(code=code_str)
                banque.nom_banque = nom_banque_str
                banque.save()
                updated += 1
            except CodeBanque.DoesNotExist:
                not_found.append(code_str)

        self.stdout.write(self.style.SUCCESS(f"✅ {updated} banques mises à jour."))
        if not_found:
            self.stdout.write(self.style.WARNING(f"⚠️ Codes non trouvés : {', '.join(not_found)}"))
