# Generated by Django 4.0.5 on 2023-06-06 21:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0016_alter_sale_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='commission',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='gross_sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_number',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='sale',
            name='shipping_cost',
            field=models.IntegerField(default=0),
        ),
    ]