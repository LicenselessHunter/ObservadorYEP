from django import forms #Se está importando la creación de forms de django para que podamos crear nuestro propio model form.
from . import models #Desde "."(directorio actual) se va a importar "models.py"


class SaleForm(forms.ModelForm):
	class Meta:
		model = models.sale
		fields = ['SKU', 'quantity', 'gross_sales', 'sale_number', 'commission', 'shipping_cost', 'sale_date']

		labels = {
			'quantity':'Cantidad',
			'gross_sales':'Venta bruta',
			'sale_number':'Número de venta',
			'commission':'Comisión',
			'shipping_cost':'Costo de envío',
			'sale_date':'Fecha de venta',
		}


class define_marketplace_for_sales_group(forms.ModelForm):
	class Meta:
		model = models.Sales_group
		fields = ['sale_marketplace', 'additional_note']

		labels = {
			'sale_marketplace':'Canal de venta',
			'additional_note':'Nota adicional',
		}

		widgets = {
			'additional_note': forms.Textarea(attrs={"rows":"5", "maxlength":"350", "cols":"48"})
		}