from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.
from django.db.models import Q


ACTIVE_INACTIVE = (
	('Activo', 'Activo'),
	('Inactivo', 'Inactivo')
)

Singular_Pack = (
	('Singular', 'Singular'),
	('PACK', 'PACK')
)

CLASSIFICATION = (
	('Elctrónica', 'Elctrónica'),
	('Ejercicio', 'Ejercicio'),
	('Joyeria', 'Joyeria'),
	('Sin clasificación', 'Sin clasificación')
)

class Product(models.Model): #Representación de la tabla de la database.
	SKU = models.CharField(max_length=20, unique=True) #CharField se usa para textos cortos, tiene un máximo de 30 caracteres.
	Description = models.CharField(max_length=70)
	classification = models.CharField(max_length=20, choices=CLASSIFICATION, null=True, default='Sin clasificación') 	
	product_image = models.ImageField(default='productDefault.png')
	STATE = models.CharField(max_length=10, choices=ACTIVE_INACTIVE, null=True, default='Activo')
	Product_type = models.CharField(max_length=10, choices=Singular_Pack, null=True, default='Singular')

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='ProductCreated_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, related_name='ProductValidated_by')
	validation_date = models.DateTimeField(default=None, null=True, blank=True)

	def __str__(self):   #Esta función va a definir como se van a ver los productos de la base de datos en la sección de admin y en el shell.
		return self.SKU  #En este caso los productos se van a mostrar con sus titulos.


class PackRelation(models.Model):
	SKU_PACK = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pack_sku', default=None, null=True)
	SKU_CHILD = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to=Q(STATE = 'Activo') & Q(Product_type= 'Singular') & Q(validation = True), related_name='singular_sku', default=None, null=True)
	CHILD_QUANTITY = models.PositiveIntegerField(default=0)




class ModifyProduct_Request(models.Model):
	id_product = models.ForeignKey(Product, to_field='id', on_delete=models.CASCADE, default=None)

	past_Description = models.CharField(max_length=70)
	past_classification = models.CharField(max_length=20, choices=CLASSIFICATION, null=True, default='Sin clasificación')
	past_product_image = models.ImageField(default='productDefault.png')

	modified_Description = models.CharField(max_length=70)
	modified_classification = models.CharField(max_length=20, choices=CLASSIFICATION, null=True, default='Sin clasificación')
	modified_product_image = models.ImageField(default='productDefault.png')

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='ModificationProduct_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='ModificationProduct_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)

class DeactivationProduct_Request(models.Model):
	id_product = models.ForeignKey(Product, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationProduct_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationProduct_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)


class RestoreProduct_Request(models.Model):
	id_product = models.ForeignKey(Product, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestoreProduct_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestoreProduct_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)