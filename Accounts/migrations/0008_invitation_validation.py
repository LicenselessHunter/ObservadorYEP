# Generated by Django 4.0.5 on 2023-06-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_rename_invitation_date_invitation_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='validation',
            field=models.BooleanField(default=False),
        ),
    ]
