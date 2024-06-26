# Generated by Django 4.0.5 on 2023-05-07 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_Type', models.CharField(choices=[('Administrador', 'Administrador'), ('Trabajador', 'Trabajador')], max_length=15, null=True)),
                ('profile_image', models.ImageField(default='userDefault.png', upload_to='')),
                ('document_number', models.CharField(blank=True, max_length=20)),
                ('cellphone_number', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
