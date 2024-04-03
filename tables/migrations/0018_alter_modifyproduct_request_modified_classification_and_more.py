# Generated by Django 4.0.5 on 2023-07-23 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0017_alter_modifyproduct_request_modified_classification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modifyproduct_request',
            name='modified_classification',
            field=models.CharField(choices=[('Elctrónica', 'Elctrónica'), ('Ejercicio', 'Ejercicio'), ('Joyeria', 'Joyeria'), ('Sin clasificación', 'Sin clasificación')], default='Sin clasificación', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='modifyproduct_request',
            name='past_classification',
            field=models.CharField(choices=[('Elctrónica', 'Elctrónica'), ('Ejercicio', 'Ejercicio'), ('Joyeria', 'Joyeria'), ('Sin clasificación', 'Sin clasificación')], default='Sin clasificación', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='classification',
            field=models.CharField(choices=[('Elctrónica', 'Elctrónica'), ('Ejercicio', 'Ejercicio'), ('Joyeria', 'Joyeria'), ('Sin clasificación', 'Sin clasificación')], default='Sin clasificación', max_length=20, null=True),
        ),
    ]
