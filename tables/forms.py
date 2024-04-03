from django import forms #Se está importando la creación de forms de django para que podamos crear nuestro propio model form.
from . import models #Desde "."(directorio actual) se va a importar "models.py"


class ProductForm(forms.ModelForm): #Esta clase va a representar el producto, va a heredar de "forms.ModelForm"
	class Meta: #Esta clase va a contener los campos o elementos que queremos mostrar en el form.
		model = models.Product #El model que vamos a usar, va a ser igual a la clase Producto de "models.py"
		fields = ['product_image', 'SKU', 'Description', 'classification'] 

		labels = {
			'product_image':'Imagen',
			'SKU':'SKU *',
			'Description':'Descripción *',
			'classification':'Clasificación',
		}

class ProductEditForm(forms.ModelForm): #Esta clase va a representar el producto, va a heredar de "forms.ModelForm"
	class Meta: #Esta clase va a contener los campos o elementos que queremos mostrar en el form.
		model = models.Product #El model que vamos a usar, va a ser igual a la clase Producto de "models.py"
		fields = ['product_image', 'Description', 'classification'] 

		labels = {
			'product_image':'Imagen',
			'Description':'Descripción',
			'classification':'Clasificación',
		}

class PACK_Form(forms.ModelForm):
	class Meta:
		model = models.PackRelation
		fields = ['SKU_CHILD', 'CHILD_QUANTITY']

		labels = {
			'SKU_CHILD':'SKU hijo *',
			'CHILD_QUANTITY':'Cantidad del SKU hijo *',
		}


		