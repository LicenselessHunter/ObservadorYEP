from django.db import models
from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.
from django.utils.timezone import now

# Create your models here.

TYPE_OF_USER = (
	('Administrador', 'Administrador'),
	('Trabajador', 'Trabajador')
)

#El model Profile se crea con el proposito de que se relacione con una relación "OneToOne" con el model implicito 'User'. Este model adicional servira para agregar atributos adicionales a las cuentas del sistema, aparte de las ya especificadas en el model implicito 'User'
class Profile(models.Model): 
	user = models.OneToOneField(User, on_delete=models.CASCADE) #Este campo se relacionara con una relación "uno a uno" con las cuentas del modelo 'User', cada elemento de 'User' estara relacionado a uno y solo un elemento de 'Profile'. Lo mismo al revés. 
	user_Type = models.CharField(max_length=15, choices=TYPE_OF_USER, null=True) #Tipo de usuario: Administrador o Trabajador
	profile_image = models.ImageField(default='userDefault.png') #La imágen de perfil
	document_number = models.CharField(max_length=20, blank=True)
	cellphone_number = models.CharField(max_length=20, blank= True)

	#def __str__(self):   
	#	return self.user

class DeactivationUser_Request(models.Model):
	id_user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationUser_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='DeactivationUser_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)


class RestoreUser_Request(models.Model):
	id_user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, default=None)

	created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestorePUser_Request_Created_by')
	created_date = models.DateTimeField(default=now)

	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='RestoreUser_Request_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)

class Invitation(models.Model):
	user_Type = models.CharField(max_length=15, choices=TYPE_OF_USER, null=True)
	code = models.CharField(max_length=10)
	email = models.EmailField()
	created_date = models.DateTimeField(default=now)
	User_sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	validation = models.BooleanField(default=False)
	validation_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name='Invitation_Validated_by')
	validation_date = models.DateTimeField(default=None, null=True)

