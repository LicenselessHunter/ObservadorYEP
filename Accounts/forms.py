from django import forms #Se está importando la creación de forms de django para que podamos crear nuestro propio model form.
from . import models #Desde "."(directorio actual) se va a importar "models.py"

from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.

class InvitationForm(forms.ModelForm):
	class Meta:
		model = models.Invitation
		fields = ['email', 'user_Type']

		labels = {
			'user_Type':'Tipo de usuario',
		}

class Invitation_SignUpForm(forms.ModelForm):
	class Meta:
		model = models.Invitation
		fields = ['email', 'code']

		labels = {
			'code':'Código',
		}


#FORMS PARA ACTUALIZACIÓN DE PERFILES PROPIOS DE USUARIO
#LA CUENTAS DEL SISTEMA SE COMPONEN DE ATRIBUTOS DEL MODEL IMPLICITO 'User' y el model 'Profile', este es el motivo de porque las cuentas necesitan dos forms.
class MyUserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']

class MyProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['profile_image', 'document_number', 'cellphone_number']

		labels = {
			'profile_image':'Imagen de perfil',
			'document_number':'N° de documento',
			'cellphone_number':'Celular',
		}