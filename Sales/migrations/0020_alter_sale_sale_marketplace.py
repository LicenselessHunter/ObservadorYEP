# Generated by Django 4.0.5 on 2023-06-28 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplaces', '0009_alter_modifymarketplace_request_modified_referencial_description_and_more'),
        ('Sales', '0019_alter_sale_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_marketplace',
            field=models.ForeignKey(default=None, limit_choices_to=models.Q(('STATE', 'Activo'), ('validation', True)), null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplaces.marketplace', to_field='Marketplace_name'),
        ),
    ]