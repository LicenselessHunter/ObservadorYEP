# Generated by Django 4.0.5 on 2023-07-22 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0012_deactivationproduct_request_additional_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='restoreproduct_request',
            name='additional_note',
            field=models.CharField(blank=True, max_length=350),
        ),
    ]
