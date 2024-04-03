from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.
from django import forms

ACTIVE_INACTIVE = (
	('Activo', 'Activo'),
	('Inactivo', 'Inactivo')
)

class Marketplace(models.Model):
	marketplace_image = models.ImageField(default='marketplaceDefault.png')
	Marketplace_name = models.CharField(max_length=30, unique=True)

	referencial_description = models.CharField(max_length=350, blank=True)

	STATE = models.CharField(max_length=10, choices=ACTIVE_INACTIVE, null=True, default='Activo')

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='MarketplaceCreated_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='MarketplaceValidated_by')
	validation_date = models.DateTimeField(default=None, null=True)

	def __str__(self):
		return str(self.Marketplace_name) #Esto es para que los ForeignKey que hacen referencia a este model, muestren en el nombre del canal de venta en el frontend en lugar del objeto en sí. Sin esto, el campo se muestra como "Marketplace object" en el frontend.


class ModifyMarketplace_Request(models.Model):
	id_marketplace = models.ForeignKey(Marketplace, to_field='id', on_delete=models.CASCADE, default=None)

	past_marketplace_image = models.ImageField(default='marketplaceDefault.png')
	past_referencial_description = models.CharField(max_length=350, blank=True)

	modified_marketplace_image = models.ImageField(default='marketplaceDefault.png')
	modified_referencial_description = models.CharField(max_length=350, blank=True)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='ModificationMarketplace_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='ModificationMarketplace_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)


class DeactivationMarketplace_Request(models.Model):
	id_marketplace = models.ForeignKey(Marketplace, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationMarketplace_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationMarketplace_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)


class RestoreMarketplace_Request(models.Model):
	id_marketplace = models.ForeignKey(Marketplace, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestoreMarketplace_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestoreMarketplace_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)