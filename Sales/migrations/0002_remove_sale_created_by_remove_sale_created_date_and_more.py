# Generated by Django 4.0.5 on 2023-05-19 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='created_date',
        ),
        migrations.AddField(
            model_name='sales_group',
            name='created_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='SaleCreated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sales_group',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
