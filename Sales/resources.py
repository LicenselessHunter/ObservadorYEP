from import_export import resources, fields
from . import models #Desde "."(directorio actual) se va a importar "models.py"
from marketplaces.models import Marketplace
from tables.models import Product
from import_export.widgets import ForeignKeyWidget
from django.db.models import F
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from . import views

class SalesAdminImportExport(resources.ModelResource):

	SKU = fields.Field(
		column_name='SKU',
		attribute='SKU',
		widget=ForeignKeyWidget(Product, 'SKU')) #Esto es uno de los widgets de la biblioteca, esto se usa cuando se tiene un campo como foreign key, aqui se esta diciendo que el campo SKU de Intake referencia al campo SKU de Product.

	sale_marketplace = fields.Field(
		column_name='sale_marketplace',
		attribute='sale_marketplace',
		widget=ForeignKeyWidget(Marketplace, 'Marketplace_name'))


	class Meta:
		model = models.sale

class Group_saleAdminImportExport(resources.ModelResource):

	sale_marketplace = fields.Field(
		column_name='sale_marketplace',
		attribute='sale_marketplace',
		widget=ForeignKeyWidget(Marketplace, 'Marketplace_name'))

	created_by = fields.Field(
		column_name='created_by',
		attribute='created_by',
		widget=ForeignKeyWidget(User, 'username'))

	Compared_by = fields.Field(
		column_name='Compared_by',
		attribute='Compared_by',
		widget=ForeignKeyWidget(User, 'username'))

	validation_by = fields.Field(
		column_name='validation_by',
		attribute='validation_by',
		widget=ForeignKeyWidget(User, 'username'))


	class Meta:
		model = models.Sales_group

class SalesResourceImport(resources.ModelResource):

	SKU = fields.Field(
		column_name='SKU',
		attribute='SKU',
		widget=ForeignKeyWidget(Product, 'SKU')) #Esto es uno de los widgets de la biblioteca, esto se usa cuando se tiene un campo como foreign key, aqui se esta diciendo que el campo SKU de Intake referencia al campo SKU de Product.

	'''
	sale_marketplace = fields.Field(
		column_name='sale_marketplace',
		attribute='sale_marketplace',
		widget=ForeignKeyWidget(Marketplace, 'Marketplace_name'))
	'''

	cantidad = fields.Field(attribute='quantity')
	venta_bruta = fields.Field(attribute='gross_sales')
	numero_venta = fields.Field(attribute='sale_number')
	fecha_venta = fields.Field(attribute='sale_date')
	comision = fields.Field(attribute='commission')
	costo_despacho = fields.Field(attribute='shipping_cost')


	def before_import_row(self, row, row_number=None, **kwargs):
	
		errors = [] #Lista que contendra los errores de cada fila


		#LEVANTAMIENTO DE ERROR CAMPO "SKU"
		try:
			Product.objects.get(SKU = row['SKU'])

		except:

			errors.append(str(Exception("SKU, " + row['SKU'] + ", no existe")))

		else:

			if Product.objects.get(SKU = row['SKU']).STATE == "Inactivo":
				errors.append(str(Exception("SKU, " + row['SKU'] + ", corresponde a un producto desactivado")))

			if Product.objects.get(SKU = row['SKU']).validation == False:
				errors.append(str(Exception("SKU, " + row['SKU'] + ", corresponde a un producto aún en espera de validación")))


		#LEVANTAMIENTO DE ERROR CAMPO "Fecha"
		
		try:
			fecha_venta_aux = str(row['fecha_venta'])
			fecha_venta_aux = fecha_venta_aux.replace(" 00:00:00", "")
			datetime.strptime(fecha_venta_aux, '%Y-%m-%d')

		except: #Si la fecha actual no tiene el formato solicitado.
		
			errors.append(str(Exception("Fecha inválida")))
		

	

		#LEVANTAMIENTO DE ERROR CAMPO "Comisión"
		
		try:
			int(row['comision']) #Se intenta ver si 'Comision' es un entero. Aqui se ira al except si 'Comision' es un string por ejemplo, pero si es flotante lo deja pasar.
			
		
		except ValueError:
			#errors.append(str(Exception("Comisión debe ser 0 o un número positivo entero"))) #Esto es por si "row['Comision'])" no es un número (Dato vacío, sring, etc)
			errors.append(str(Exception("Comisión debe ser 0 o un número positivo entero")))
		else: #Esto es para detectar si el número es efectivamente entero

			if row['comision'].is_integer(): #Si el número es entero
				#pass
				if row['comision'] < 0:
					#errors.append(str(Exception("Comisión debe ser 0 o un número positivo entero")))
					errors.append(str(Exception("Comisión debe ser 0 o un número positivo entero")))


			else: #Si el número no es entero
				errors.append(str(Exception("Comisión debe ser 0 o un número positivo entero")))
				#errors.append(str(Exception("Comisión no es un número entero. Canal de venta: " + row['Canal_venta'])))
		

				#row['comision'] = round(row['comision'])



		#LEVANTAMIENTO DE ERROR CAMPO "costo_despacho"
		
		try:
			int(row['costo_despacho']) #Se intenta ver si 'costo_despacho' es un entero. Aqui se ira al except si 'costo_despacho' es un string por ejemplo, pero si es flotante lo deja pasar.
			
		
		except ValueError:

			errors.append(str(Exception("Costo de despacho debe ser 0 o un número positivo entero")))
		else: #Esto es para detectar si el número es efectivamente entero

			if row['costo_despacho'].is_integer(): #Si el número es entero

				if row['costo_despacho'] < 0:

					errors.append(str(Exception("Costo de despacho debe ser 0 o un número positivo entero")))


			else: #Si el número no es entero
				errors.append(str(Exception("Costo de despacho debe ser 0 o un número positivo entero")))




		#LEVANTAMIENTO DE ERROR CAMPO "venta_bruta"
		
		try:
			int(row['venta_bruta']) #Se intenta ver si 'venta_bruta' es un entero. Aqui se ira al except si 'venta_bruta' es un string por ejemplo, pero si es flotante lo deja pasar.
			
		
		except ValueError:

			errors.append(str(Exception("Venta bruta debe ser 0 o un número positivo entero")))
		else: #Esto es para detectar si el número es efectivamente entero

			if row['venta_bruta'].is_integer(): #Si el número es entero

				if row['venta_bruta'] < 0:

					errors.append(str(Exception("Venta bruta debe ser 0 o un número positivo entero")))


			else: #Si el número no es entero
				errors.append(str(Exception("Venta bruta debe ser 0 o un número positivo entero")))






		#LEVANTAMIENTO DE ERROR CAMPO "cantidad"
		
		try:
			int(row['cantidad']) #Se intenta ver si 'cantidad' es un entero. Aqui se ira al except si 'cantidad' es un string por ejemplo, pero si es flotante lo deja pasar.
			
		
		except ValueError:

			errors.append(str(Exception("Cantidad debe ser número positivo entero mayor a 0")))
		else: #Esto es para detectar si el número es efectivamente entero

			if row['cantidad'].is_integer(): #Si el número es entero

				if row['cantidad'] <= 0:

					errors.append(str(Exception("Cantidad debe ser número positivo entero mayor a 0")))


			else: #Si el número no es entero
				errors.append(str(Exception("Cantidad debe ser número positivo entero mayor a 0")))






		#LEVANTAMIENTO DE ERROR CAMPO "numero_venta"
		row['numero_venta'] = str(row['numero_venta']) #Se hace esto por si el campo es un número

		if len(row['numero_venta']) == 0 or len(row['numero_venta']) > 40:

			errors.append(str(Exception("N° de venta debe tener entre 1 a 40 carácteres")))

		add_sale_query = models.sale.objects.filter(sale_number = row['numero_venta'], SKU = row['SKU'], Sale_group__sale_marketplace = kwargs['marketplaceInstance'])
		existent_row = str(row['SKU']) + ' ' + str(row['numero_venta'])
		#print(add_sale_query)
		if add_sale_query.exists():

			Already_Existing_Sale = models.sale.objects.get(sale_number = row['numero_venta'], SKU = row['SKU'], Sale_group__sale_marketplace = kwargs['marketplaceInstance'])
			
			if existent_row in kwargs['existent_sale_on_file_List']:
				errors.append(str(Exception("No se pueden tener dos o más líneas en el archivo excel con el mismo SKU y Número de venta")))


			elif Already_Existing_Sale.Sale_group.validation == False:
				errors.append(str(Exception("Ya existe un registro con el SKU, Número de venta y canal de venta especificados en esta línea. El registro existente en cuestión es una venta en espera de id: " + str(Already_Existing_Sale.id) + " dentro del grupo de venta de id: " + str(Already_Existing_Sale.Sale_group.id))))

			elif Already_Existing_Sale.Sale_group.validation == True:
				errors.append(str(Exception("Ya existe un registro con el SKU, Número de venta y canal de venta especificados en esta línea. El registro existente en cuestión es una venta finalizada de id: " + str(Already_Existing_Sale.id) + " dentro del grupo de venta de id: " + str(Already_Existing_Sale.Sale_group.id))))

		else:

			kwargs['existent_sale_on_file_List'].append(existent_row)
			print(kwargs['existent_sale_on_file_List'])



		#SI ES QUE LA LISTA "errors" TIENE CONTENIDO
		if errors:

			errors = "--".join(errors) #Se usa este join para sacar los [] de la lista de errores de esta fila, además entre cada error de la fila se agregara el signo "--" para que después en views.py se puedan separar correctamente, puede ser cualquier signo enrealidad.

			raise Exception(errors) #Se levanta la lista de errors con todas las excepciones que agrupo, esto se hace asi ya que al levantar una excepción individual el programa se detiene, evitando que se puedan mostrar múltiples errores.


	def after_import_instance(self, instance, new, **kwargs):

		instance.Sale_group = kwargs['sale_groupInstance']
		#instance.sale_marketplace = kwargs['marketplaceInstance']


	class Meta:
		model = models.sale
		fields = ['id', 'SKU', 'cantidad', 'venta_bruta', 'numero_venta', 'fecha_venta', 'comision', 'costo_despacho']

		
		widgets = {
				'fecha_venta': {'format': '%d-%m-%Y'},
				}




class SalesComparisonResourceImport(resources.ModelResource):

	SKU = fields.Field(
		column_name='SKU',
		attribute='SKU',
		widget=ForeignKeyWidget(Product, 'SKU')) #Esto es uno de los widgets de la biblioteca, esto se usa cuando se tiene un campo como foreign key, aqui se esta diciendo que el campo SKU de Intake referencia al campo SKU de Product.

	'''
	sale_marketplace = fields.Field(
		column_name='sale_marketplace',
		attribute='sale_marketplace',
		widget=ForeignKeyWidget(Marketplace, 'Marketplace_name'))
	'''

	cantidad = fields.Field(attribute='quantity')
	venta_bruta = fields.Field(attribute='gross_sales')
	numero_venta = fields.Field(attribute='sale_number')
	fecha_venta = fields.Field(attribute='sale_date')
	comision = fields.Field(attribute='commission')
	costo_despacho = fields.Field(attribute='shipping_cost')


	def before_import(self, dataset, using_transactions, dry_run, **kwargs):

		if len(dataset) != kwargs['Total_sales_objects']:
			print("No tiene todas las filas")
			raise Exception("No tiene todas las filas")


	def before_import_row(self, row, row_number=None, **kwargs):

		errors = []

		row_query = models.sale.objects.filter(SKU = row['SKU'], quantity = row['cantidad'], gross_sales = row['venta_bruta'], sale_number = row['numero_venta'], sale_date = row['fecha_venta'], commission = row['comision'], shipping_cost = row['costo_despacho'], Sale_group = kwargs['Sales_group'])

		#print(str(row_query))

		if not row_query.exists():
			errors.append(str(Exception("Registro no coincidente con alguna venta del grupo")))

		#Este bloque else existe para detectar líneas validas pero repetidas en el archivo para la comparación.
		else:
			
			if str(row_query) in kwargs['AlreadyComparedList']:
				errors.append(str(Exception("Registro coincidente, pero repetido en su archivo")))

			else:
				kwargs['AlreadyComparedList'].append(str(row_query))



		if errors:
			errors = "--".join(errors) #Se usa este join para sacar los [] de la lista de errores de esta fila, además entre cada error de la fila se agregara el signo "--" para que después en views.py se puedan separar correctamente, puede ser cualquier signo enrealidad.

			raise Exception(errors) #Se levanta la lista de errors con todas las excepciones que agrupo, esto se hace asi ya que al levantar una excepción individual el programa se detiene, evitando que se puedan mostrar múltiples errores.



	class Meta:
		model = models.sale
		fields = ['id', 'SKU', 'cantidad', 'venta_bruta', 'numero_venta', 'fecha_venta', 'comision', 'costo_despacho']

		widgets = {
				'sale_date': {'format': '%d-%m-%Y'},
				}