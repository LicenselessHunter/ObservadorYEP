# Generated by Django 4.0.5 on 2023-05-26 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplaces', '0007_rename_marketplace_image_modifymarketplace_request_modified_marketplace_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplace',
            name='referencial_description',
            field=models.CharField(blank=True, max_length=350),
        ),
    ]