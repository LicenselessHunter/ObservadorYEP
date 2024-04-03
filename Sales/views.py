from django.shortcuts import render, redirect
from .models import sale, Sales_group
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required #Se importa el decorator.from django.shortcuts import render
from . import resources
from tablib import Dataset #Tablib is an MIT Licensed format-agnostic tabular dataset library, written in Python. It allows you to import, export, and manipulate tabular data sets. Advanced features include, segregation, dynamic columns, tags & filtering, and seamless format import & export. Se combinara con bilbioteca 'django-import-export'
from . import forms
from django.forms import formset_factory #Se importan los formsets
from marketplaces.models import Marketplace
from django.db.models import Sum
from django.db.models import Count
from django.core.paginator import Paginator #Se importa un paginator para tener diferentes páginas de navegación con respecto al model. Como lo que usa google.
from django.urls import reverse_lazy #It is useful for when you need to use a URL reversal before your project’s URLConf is loaded.

# Create your views here.

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def finalized_sales(request):
	
	Marketplaces = Marketplace.objects.filter(validation = True)
	DateFilterUsed = False
	MarketplaceChoosed = False
	finalized_sales = sale.objects.filter(Sale_group__validation = True).order_by('-sale_date', '-id')
	paginatorInstance = Paginator(finalized_sales, 50) #Instancia del paginator, se usara con el respectivo query y se especifica cuantas instancias de esta se quieren mostrar
	page_number = request.GET.get('page') #Esto obtiene el número de la página.
	Paginate_finalized_sales = paginatorInstance.get_page(page_number) #Esto es lo que finalmente contendra el listado de las instancias del query, el cual dependera del número de la página y el número de instancias a mostrar especificado anteriormente.

	if request.method == 'POST' and 'finalized_sales_filter' in request.POST:
		fromDate = request.POST.get('From_date')
		toDate = request.POST.get('To_date')
		marketplace_selected = request.POST.get('marketplace_select_finalizedSales')



		if not fromDate and not toDate and marketplace_selected != 'global':

			finalized_sales = sale.objects.filter(Sale_group__validation = True, Sale_group__sale_marketplace = marketplace_selected).order_by('-sale_date', '-id')
			MarketplaceChoosed = True

		elif fromDate and toDate and marketplace_selected != 'global':

			finalized_sales = sale.objects.filter(sale_date__range = [fromDate, toDate], Sale_group__validation = True, Sale_group__sale_marketplace = marketplace_selected).order_by('-sale_date', '-id')
			MarketplaceChoosed = True
			DateFilterUsed = True

		elif fromDate and toDate and marketplace_selected == 'global':
			finalized_sales = sale.objects.filter(sale_date__range = [fromDate, toDate], Sale_group__validation = True).order_by('-sale_date', '-id')
			DateFilterUsed = True

		context = {
			'finalized_sales':finalized_sales,
			'Paginate_finalized_sales':Paginate_finalized_sales,
			'Marketplaces':Marketplaces,
			'DateFilterUsed':DateFilterUsed,
			'MarketplaceChoosed':MarketplaceChoosed,
			'fromDate':fromDate,
			'toDate':toDate,
			'marketplace_selected':marketplace_selected,
		}


	else:
		

		context = {
			'finalized_sales':finalized_sales,
			'Paginate_finalized_sales':Paginate_finalized_sales,
			'Marketplaces':Marketplaces,
			'DateFilterUsed':DateFilterUsed,
			'MarketplaceChoosed':MarketplaceChoosed,
		}

	return render(request, "Sales/finalized_sales.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def sale_detail(request, id):
	saleInstance = sale.objects.get(id=id)


	return render(request, "Sales/sale_detail.html", {'sale':saleInstance})


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def sales_on_standby(request):

	unvalidated_sales_groups = Sales_group.objects.filter(validation = False).order_by('-id')

	define_marketplace_for_sales_group_form = forms.define_marketplace_for_sales_group()


	if request.method == 'POST' and 'Import' in request.POST:

		sale_resource = resources.SalesResourceImport() #product_resource va a representar el resource 'ProductResourceImport()'.
		dataset = Dataset()
		new_sales = request.FILES['ImportData'] #'request.FILES['ImportData']' Contiene el archivo subido en la pagina para importación.

		imported_data = dataset.load(new_sales.read(),format='xlsx') #Aqui se carga y lee el archivo subido en la página y se especifica su formato.

		marketplace_input = request.POST.get('sale_marketplace')
		additional_note_input = request.POST.get('additional_note')
		marketplaceInstance = Marketplace.objects.get(Marketplace_name = marketplace_input)

		sale_group_instance = Sales_group.objects.create(created_by = request.user, sale_marketplace = marketplaceInstance, additional_note = additional_note_input)
		

		# Testing data import
		result = sale_resource.import_data(dataset, dry_run=True, sale_groupInstance = sale_group_instance, marketplaceInstance = marketplaceInstance, existent_sale_on_file_List = []) #Se testea el data, se verifica que las propiedades de los campos sean correctos, los formatos, etc.

		if not result.has_errors(): #Si pasa el testeo.
			# Import now
			sale_resource.import_data(dataset, dry_run=False, sale_groupInstance = sale_group_instance, marketplaceInstance = marketplaceInstance, existent_sale_on_file_List = [])
			
			#sale_group_instance.save()
			messages.success(request, 'Grupo de venta creado con éxito, queda a espera de comparación y validación')

			return redirect ("Sales:sales_on_standby")

		elif result.has_errors():

			ErrorDict = {}

			for line, errors in result.row_errors(): #Se van a recorrer a través de las líneas y errores de "row_errors", el cual contiene los errores especificos de la importación junto a las líneas donde ocurrio.
				for error in errors:
					ErrorDict[line] = [] #Se va a agregar una lista al diccionario "ErrorDict", con el key representando al line de row_errors()
					for a in str(error.error).split("--"): #Los errores de line van a ser separados entre si por el simbolo "--"
						ErrorDict[line].append(a) #Cada error individual de line será agregado a la lista representante del diccionario "ErrorDict"



			sale_group_instance.delete()

			context = {
			
				'define_marketplace_for_sales_group_form':define_marketplace_for_sales_group_form,
				'unvalidated_sales_groups':unvalidated_sales_groups,
				'result':result,
				'ErrorDict':ErrorDict,
			}

			return render(request, "Sales/sales_on_standby.html", context)

	context = {

		'define_marketplace_for_sales_group_form':define_marketplace_for_sales_group_form,
		'unvalidated_sales_groups':unvalidated_sales_groups,
	
	}

	return render(request, "Sales/sales_on_standby.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def SalesGroup_detail(request, id):
	Sales_group_instance = Sales_group.objects.get(id = id)


	Sales_related_to_group = sale.objects.filter(Sale_group = Sales_group_instance).order_by('-sale_date', '-id')


	Totals = sale.objects.filter(Sale_group = Sales_group_instance).aggregate(Total_gross_sales = Sum('gross_sales'), Total_commission = Sum('commission'), Total_shipping_cost = Sum('shipping_cost'), Total_sales_quantity = Sum('quantity'))

	Total_sales_objects = sale.objects.filter(Sale_group = Sales_group_instance).count()


	if request.method == 'POST' and 'import_comparison' in request.POST:

		sales_comparison_resource = resources.SalesComparisonResourceImport()
		dataset = Dataset()
		sales_for_comparison = request.FILES['ImportData'] #'request.FILES['ImportData']' Contiene el archivo subido en la pagina para importación.

		imported_data = dataset.load(sales_for_comparison.read(),format='xlsx') #Aqui se carga y lee el archivo subido en la página y se especifica su formato.


		result = sales_comparison_resource.import_data(dataset, dry_run=True, Sales_group=Sales_group_instance, AlreadyComparedList = [], Total_sales_objects = Total_sales_objects) #AlreadyComparedList sirve para detectar líneas validas pero repetidas en el archivo excel.

		if not result.has_errors(): #Si pasa el testeo.
			Sales_group_instance.Compared = True
			Sales_group_instance.Compared_by = request.user
			Sales_group_instance.Compared_date = now()			

			Sales_group_instance.save()
			messages.success(request, 'Comparación realizada con éxito, el grupo quedará a espera de ser validado por un Administrador')

		elif result.has_errors():

			Same_sales_quantity = True

			if (len(imported_data) != Total_sales_objects):
				#messages.error(request, 'Su archivo de comparación no contiene la misma cantidad de filas que el grupo de venta que desea comparar')
				Same_sales_quantity = False

			ErrorDict = {}

			for line, errors in result.row_errors(): #Se van a recorrer a través de las líneas y errores de "row_errors", el cual contiene los errores especificos de la importación junto a las líneas donde ocurrio.
				for error in errors:
					ErrorDict[line] = [] #Se va a agregar una lista al diccionario "ErrorDict", con el key representando al line de row_errors()
					for a in str(error.error).split("--"): #Los errores de line van a ser separados entre si por el simbolo "--"
						ErrorDict[line].append(a) #Cada error individual de line será agregado a la lista representante del diccionario "ErrorDict"


			context = {
				'Same_sales_quantity':Same_sales_quantity,
				'Totals':Totals,
				'Total_sales_objects':Total_sales_objects,
				'Sales_group_instance':Sales_group_instance,
				'Sales_related_to_group':Sales_related_to_group,
				'result':result,
				'ErrorDict':ErrorDict,
			}

			return render(request, "Sales/SalesGroup_detail.html", context)


	if request.method == 'POST' and 'import_admin_comparison' in request.POST:

		sales_comparison_resource = resources.SalesComparisonResourceImport()
		dataset = Dataset()
		sales_for_comparison = request.FILES['ImportData'] #'request.FILES['ImportData']' Contiene el archivo subido en la pagina para importación.

		imported_data = dataset.load(sales_for_comparison.read(),format='xlsx') #Aqui se carga y lee el archivo subido en la página y se especifica su formato.


		result = sales_comparison_resource.import_data(dataset, dry_run=True, Sales_group=Sales_group_instance, AlreadyComparedList = [], Total_sales_objects = Total_sales_objects) #AlreadyComparedList sirve para detectar líneas validas pero repetidas en el archivo excel.

		if not result.has_errors(): #Si pasa el testeo.	

			messages.success(request, 'Comparación realizada con éxito, todas las ventas de su archivo coinciden')

		elif result.has_errors():

			Same_sales_quantity = True

			if (len(imported_data) != Total_sales_objects):
				#messages.error(request, 'Su archivo de comparación no contiene la misma cantidad de filas que el grupo de venta que desea comparar')
				Same_sales_quantity = False

			ErrorDict = {}

			for line, errors in result.row_errors(): #Se van a recorrer a través de las líneas y errores de "row_errors", el cual contiene los errores especificos de la importación junto a las líneas donde ocurrio.
				for error in errors:
					ErrorDict[line] = [] #Se va a agregar una lista al diccionario "ErrorDict", con el key representando al line de row_errors()
					for a in str(error.error).split("--"): #Los errores de line van a ser separados entre si por el simbolo "--"
						ErrorDict[line].append(a) #Cada error individual de line será agregado a la lista representante del diccionario "ErrorDict"


			context = {
				'Same_sales_quantity':Same_sales_quantity,
				'Totals':Totals,
				'Total_sales_objects':Total_sales_objects,
				'Sales_group_instance':Sales_group_instance,
				'Sales_related_to_group':Sales_related_to_group,
				'result':result,
				'ErrorDict':ErrorDict,
			}

			return render(request, "Sales/SalesGroup_detail.html", context)


	if request.method == 'POST' and 'validate' in request.POST:
		Sales_group_instance.validation = True
		Sales_group_instance.validation_by = request.user
		Sales_group_instance.validation_date = now()

		Sales_group_instance.save()

		messages.success(request, 'Ventas validadas con éxito')
		return redirect("Sales:finalized_sales")

	if request.method == 'POST' and 'reject' in request.POST:
		Sales_group_instance.delete()

		messages.success(request, 'Grupo de venta rechazada con éxito')
		return redirect("Sales:sales_on_standby")

	context = {
		'Totals':Totals,
		'Total_sales_objects':Total_sales_objects,
		'Sales_group_instance':Sales_group_instance,
		'Sales_related_to_group':Sales_related_to_group,
	}

	return render(request, "Sales/SalesGroup_detail.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_SalesGroups(request):

	validated_SalesGroups = Sales_group.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_SalesGroups':validated_SalesGroups,
	}

	return render(request, "Sales/validated_SalesGroups.html", context)