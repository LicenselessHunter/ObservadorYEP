from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.
from django.db.models import Q
from marketplaces.models import Marketplace
from tables.models import Product



class Sales_group(models.Model):
	validation = models.BooleanField(default=False, blank=True)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, related_name='Sales_groupValidated_by')
	validation_date = models.DateTimeField(default=None, null=True, blank=True)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, related_name='SaleCreated_by')
	created_date = models.DateTimeField(default=now, blank=True)

	Compared = models.BooleanField(default=False, blank=True)
	Compared_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, related_name='Sales_groupCompared_by')
	Compared_date = models.DateTimeField(default=None, null=True, blank=True)

	sale_marketplace = models.ForeignKey(Marketplace, to_field='Marketplace_name', limit_choices_to= Q(STATE = 'Activo') & Q(validation = True), on_delete=models.CASCADE, default=None)

	additional_note = models.CharField(max_length=350, blank=True)

class sale(models.Model):
	quantity = models.IntegerField(default=0)

	gross_sales = models.IntegerField(default=0)

	sale_number = models.CharField(max_length=40)
	sale_date = models.DateField(default=now, blank=True)
	
	commission = models.IntegerField(default=0)
	shipping_cost = models.IntegerField(default=0)

	#sale_marketplace = models.ForeignKey(Marketplace, to_field='Marketplace_name', limit_choices_to= Q(STATE = 'Activo') & Q(validation = True), on_delete=models.CASCADE, default=None, null = True)

	SKU = models.ForeignKey(Product, to_field='SKU', limit_choices_to= Q(STATE = 'Activo') & Q(validation = True), on_delete=models.CASCADE, default=None)

	Sale_group = models.ForeignKey(Sales_group, to_field='id', default=None, null=True, on_delete=models.CASCADE)
