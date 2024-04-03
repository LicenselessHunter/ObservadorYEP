from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Se importa el decorator.
from tables.models import Product
from Sales.models import sale
from django.db.models import Sum
from django.db.models import Count
from marketplaces.models import Marketplace
from django.db.models import F
from datetime import datetime, timedelta
from django.contrib.auth.models import User


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def viewHome(request):

	Total_products = Product.objects.all().count()
	Total_users = User.objects.all().count()
	Total_marketplaces = Marketplace.objects.all().count()

	Marketplaces = Marketplace.objects.filter(sales_group__validation = True, sales_group__Compared = True).annotate(Total_sales_quantity_by_marketplace=Sum('sales_group__sale__quantity'))

	context = {
		'Marketplaces':Marketplaces,
		'Total_products':Total_products,
		'Total_users':Total_users,
		'Total_marketplaces':Total_marketplaces,
	}

	return render(request, "home.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def dashboard(request):

	
	if request.method == 'POST':
		FilterUsed = True
		fromDate = request.POST.get('From_date')
		toDate = request.POST.get('To_date')

		toDate_plusOneDay = datetime.strptime(toDate, "%Y-%m-%d") + timedelta(days=1)

		Totals = sale.objects.filter(sale_date__range = [fromDate, toDate], Sale_group__validation = True, Sale_group__Compared = True).aggregate(Total_gross_sales = Sum('gross_sales'), Total_commission = Sum('commission'), Total_shipping_cost = Sum('shipping_cost'), Total_sales_quantity = Sum('quantity'))



		#--------- Este query se va a usar para los totales de los gráficos de donas --------------
		Marketplaces = Marketplace.objects.filter(sales_group__sale__sale_date__range = [fromDate, toDate], sales_group__validation = True, sales_group__Compared = True).annotate(Total_gross_sales_by_marketplace =Sum('sales_group__sale__gross_sales'), Total_commission_by_marketplace=Sum('sales_group__sale__commission'), Total_shipping_cost_by_marketplace=Sum('sales_group__sale__shipping_cost'), Total_sales_quantity_by_marketplace=Sum('sales_group__sale__quantity')) #Este query se va a usar para los totales de los gráficos de donas.



		#--------- Este query va a ser para el gráfico de línea, va a contener los índices diarios totales de cada marketplace --------------
		Marketplaces_sales_byDay = Marketplace.objects.filter(sales_group__sale__sale_date__range = [fromDate, toDate], sales_group__validation = True, sales_group__Compared = True).values('Marketplace_name', 'sales_group__sale__sale_date').order_by('sales_group__sale__sale_date').annotate(gross_sales_byDay = Sum('sales_group__sale__gross_sales'), commission_byDay = Sum('sales_group__sale__commission'), shipping_cost_byDay = Sum('sales_group__sale__shipping_cost'), quantity_byDay = Sum('sales_group__sale__quantity')) 
		'''
		EXLICACIÓN DE 'Marketplaces_sales_byDay'

		1. values() --> Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable. Each of those dictionaries represents an object, with the keys corresponding to the attribute names of model objects. Para usar estos valores en el template, se pueden usar tal cuál con el nombre que tienen.

		2. order_by() --> Se ordena el query con el parámetro puesto aquí, para este caso, se va a ordenar el query desde la fecha más vieja de venta
		
		3. annotate() --> Calculates summary values for each item in the queryset
		
		'''

		#Sales_byDay = sale.objects.filter(Sale_group__validation = True, Sale_group__Compared = True).values('sale_date', 'Sale_group__sale_marketplace').order_by('sale_date').annotate(Sum=Sum('gross_sales'))


		#--------- Este query se va a usar para el gráfico de línea, se va a usar para los labels de las fechas --------------
		Sales_TotalbyDay = sale.objects.filter(sale_date__range = [fromDate, toDate], Sale_group__validation = True, Sale_group__Compared = True).values('sale_date').order_by('sale_date').annotate(gross_sales_byDay=Sum('gross_sales'), commission_byDay = Sum('commission'), shipping_cost_byDay = Sum('shipping_cost'), quantity_byDay = Sum('quantity'))




		#--------- queries se van a usar para los listados de mayor a menor de los productos y sus índices --------------
		products = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).annotate(gross_sale_byProduct = Sum('sale__gross_sales')).order_by('-gross_sale_byProduct')

		productsByMarketplace = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(gross_sale_byProduct = Sum('sale__gross_sales')).order_by('-gross_sale_byProduct')




		products_commission = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).annotate(commission_byProduct = Sum('sale__commission')).order_by('-commission_byProduct')

		productsByMarketplace_commission = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(commission_byProduct = Sum('sale__commission')).order_by('-commission_byProduct')




		products_shipping_cost = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).annotate(shipping_cost_byProduct = Sum('sale__shipping_cost')).order_by('-shipping_cost_byProduct')

		productsByMarketplace_shipping_cost = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(shipping_cost_byProduct = Sum('sale__shipping_cost')).order_by('-shipping_cost_byProduct')




		products_quantity = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).annotate(quantity_byProduct = Sum('sale__quantity')).order_by('-quantity_byProduct')

		productsByMarketplace_quantity = Product.objects.filter(sale__sale_date__range = [fromDate, toDate], validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(quantity_byProduct = Sum('sale__quantity')).order_by('-quantity_byProduct')




		
		context = {
			'Totals':Totals,
			'Marketplaces':Marketplaces,
			'products':products,
			'productsByMarketplace':productsByMarketplace,
			'Marketplaces_sales_byDay':Marketplaces_sales_byDay,
			'Sales_TotalbyDay':Sales_TotalbyDay,


			'products_commission':products_commission,
			'productsByMarketplace_commission':productsByMarketplace_commission,


			'products_shipping_cost':products_shipping_cost,
			'productsByMarketplace_shipping_cost':productsByMarketplace_shipping_cost,


			'products_quantity':products_quantity,
			'productsByMarketplace_quantity':productsByMarketplace_quantity,

			'FilterUsed':FilterUsed,
			'fromDate':fromDate,
			'toDate':toDate,


		}


	else:
		FilterUsed = False

		Totals = sale.objects.filter(Sale_group__validation = True, Sale_group__Compared = True).aggregate(Total_gross_sales = Sum('gross_sales'), Total_commission = Sum('commission'), Total_shipping_cost = Sum('shipping_cost'), Total_sales_quantity = Sum('quantity'))

		print(Totals['Total_sales_quantity'])
		#--------- Este query se va a usar para los totales de los gráficos de donas --------------
		Marketplaces = Marketplace.objects.filter(sales_group__validation = True, sales_group__Compared = True).annotate(Total_gross_sales_by_marketplace =Sum('sales_group__sale__gross_sales'), Total_commission_by_marketplace=Sum('sales_group__sale__commission'), Total_shipping_cost_by_marketplace=Sum('sales_group__sale__shipping_cost'), Total_sales_quantity_by_marketplace=Sum('sales_group__sale__quantity')) #Este query se va a usar para los totales de los gráficos de donas.



		#--------- Este query va a ser para el gráfico de línea, va a contener los índices diarios totales de cada marketplace --------------
		Marketplaces_sales_byDay = Marketplace.objects.filter(sales_group__validation = True, sales_group__Compared = True).values('Marketplace_name', 'sales_group__sale__sale_date').order_by('sales_group__sale__sale_date').annotate(gross_sales_byDay = Sum('sales_group__sale__gross_sales'), commission_byDay = Sum('sales_group__sale__commission'), shipping_cost_byDay = Sum('sales_group__sale__shipping_cost'), quantity_byDay = Sum('sales_group__sale__quantity')) 
		'''
		EXLICACIÓN DE 'Marketplaces_sales_byDay'

		1. values() --> Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable. Each of those dictionaries represents an object, with the keys corresponding to the attribute names of model objects. Para usar estos valores en el template, se pueden usar tal cuál con el nombre que tienen.

		2. order_by() --> Se ordena el query con el parámetro puesto aquí, para este caso, se va a ordenar el query desde la fecha más vieja de venta
		
		3. annotate() --> Calculates summary values for each item in the queryset
		
		'''

		#Sales_byDay = sale.objects.filter(Sale_group__validation = True, Sale_group__Compared = True).values('sale_date', 'Sale_group__sale_marketplace').order_by('sale_date').annotate(Sum=Sum('gross_sales'))


		#--------- Este query se va a usar para el gráfico de línea, se va a usar para los labels de las fechas --------------
		Sales_TotalbyDay = sale.objects.filter(Sale_group__validation = True, Sale_group__Compared = True).values('sale_date').order_by('sale_date').annotate(gross_sales_byDay=Sum('gross_sales'), commission_byDay = Sum('commission'), shipping_cost_byDay = Sum('shipping_cost'), quantity_byDay = Sum('quantity'))




		#--------- queries se van a usar para los listados de mayor a menor de los productos y sus índices --------------
		products = Product.objects.filter(validation = True, sale__Sale_group__validation = True).annotate(gross_sale_byProduct = Sum('sale__gross_sales')).order_by('-gross_sale_byProduct')

		productsByMarketplace = Product.objects.filter(validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(gross_sale_byProduct = Sum('sale__gross_sales')).order_by('-gross_sale_byProduct')




		products_commission = Product.objects.filter(validation = True, sale__Sale_group__validation = True).annotate(commission_byProduct = Sum('sale__commission')).order_by('-commission_byProduct')

		productsByMarketplace_commission = Product.objects.filter(validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(commission_byProduct = Sum('sale__commission')).order_by('-commission_byProduct')




		products_shipping_cost = Product.objects.filter(validation = True, sale__Sale_group__validation = True).annotate(shipping_cost_byProduct = Sum('sale__shipping_cost')).order_by('-shipping_cost_byProduct')

		productsByMarketplace_shipping_cost = Product.objects.filter(validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(shipping_cost_byProduct = Sum('sale__shipping_cost')).order_by('-shipping_cost_byProduct')




		products_quantity = Product.objects.filter(validation = True, sale__Sale_group__validation = True).annotate(quantity_byProduct = Sum('sale__quantity')).order_by('-quantity_byProduct')

		productsByMarketplace_quantity = Product.objects.filter(validation = True, sale__Sale_group__validation = True).values('sale__Sale_group__sale_marketplace', 'SKU', 'Description').annotate(quantity_byProduct = Sum('sale__quantity')).order_by('-quantity_byProduct')




		
		context = {
			'Totals':Totals,
			'Marketplaces':Marketplaces,
			'products':products,
			'productsByMarketplace':productsByMarketplace,
			'Marketplaces_sales_byDay':Marketplaces_sales_byDay,
			'Sales_TotalbyDay':Sales_TotalbyDay,


			'products_commission':products_commission,
			'productsByMarketplace_commission':productsByMarketplace_commission,


			'products_shipping_cost':products_shipping_cost,
			'productsByMarketplace_shipping_cost':productsByMarketplace_shipping_cost,


			'products_quantity':products_quantity,
			'productsByMarketplace_quantity':productsByMarketplace_quantity,

			'FilterUsed':FilterUsed,

		}

	return render(request, "dashboard.html", context)