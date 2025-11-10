import pandas as pd
from django.core.management.base import BaseCommand
from budget_app.models import CodeBanque, CodeLocalite


class Command(BaseCommand):
    help = 'Importe les codes banques et localités depuis un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='CodeBanques.xlsx')
        
    def handle(self, *args, **kwargs):
        file_path = kwargs['excel_file']
        df = pd.read_excel(file_path, sheet_name="Feuil1")

        imported_banque = 0
        ignored_banque = 0
        for i, row in df.iterrows():
            if pd.notna(row['Code Banque']):
                code_banque = str(int(row['Code Banque'])).zfill(3)
                CodeBanque.objects.get_or_create(code=code_banque)
                imported_banque += 1
            else:
                ignored_banque += 1

        imported_localite = 0
        ignored_localite = 0
        for i, row in df.iterrows():
            if pd.notna(row['Code Localité']):
                code_localite = str(int(row['Code Localité'])).zfill(3)
                CodeLocalite.objects.get_or_create(code=code_localite)
                imported_localite += 1
            else:
                ignored_localite += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import terminé : {imported_banque} codes banques importés, {ignored_banque} ignorés. "
            f"{imported_localite} codes localités importés, {ignored_localite} ignorés."
        ))
