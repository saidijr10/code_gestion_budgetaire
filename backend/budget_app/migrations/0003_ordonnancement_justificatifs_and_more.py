# Generated by Django 5.2.3 on 2025-06-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_app', '0002_prestataire_contact_alter_prestataire_adresse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordonnancement',
            name='justificatifs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordonnancement',
            name='mode_paiement',
            field=models.CharField(choices=[('virement', 'Virement'), ('cheque', 'Chèque'), ('espece', 'Espèce')], default='virement', max_length=10),
        ),
        migrations.AddField(
            model_name='ordonnancement',
            name='objet',
            field=models.CharField(default='aucun', max_length=255),
            preserve_default=False,
        ),
    ]
