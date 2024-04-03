from django import forms #Se está importando la creación de forms de django para que podamos crear nuestro propio model form.
from . import models #Desde "."(directorio actual) se va a importar "models.py"

class MarketplaceForm(forms.ModelForm):
	class Meta: 
		model = models.Marketplace
		fields = ['Marketplace_name', 'marketplace_image', 'referencial_description']

		labels = {
			'Marketplace_name':'Nombre canal *',
			'marketplace_image':'Imagen',
			'referencial_description':'Descripción referencial',
		}

		widgets = {
			'referencial_description': forms.Textarea(attrs={"rows":"5", "maxlength":"350", "cols":"48"})
		}

class MarketplaceEditForm(forms.ModelForm): #Esta clase va a representar el producto, va a heredar de "forms.ModelForm"
	class Meta: #Esta clase va a contener los campos o elementos que queremos mostrar en el form.
		model = models.Marketplace #El model que vamos a usar, va a ser igual a la clase Producto de "models.py"
		fields = ['Marketplace_name', 'marketplace_image', 'referencial_description']

		labels = {
			'Marketplace_name':'Imagen',
			'marketplace_image':'Imagen',
			'referencial_description':'Descripción referencial',
		}

		widgets = {
			'referencial_description': forms.Textarea(attrs={"rows":"5", "maxlength":"450", "cols":"48"})
		}