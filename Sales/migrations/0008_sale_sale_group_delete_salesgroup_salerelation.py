# Generated by Django 4.0.5 on 2023-05-21 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0007_alter_sales_group_compared_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='Sale_group',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sales.sales_group'),
        ),
        migrations.DeleteModel(
            name='SalesGroup_SaleRelation',
        ),
    ]
