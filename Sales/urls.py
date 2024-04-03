from django.contrib import admin
from django.urls import path
from . import views #Referencio al archivo views para usar sus funciones.

app_name = 'Sales'

urlpatterns = [
	path('', views.finalized_sales, name='finalized_sales'),
	path('sale_detail/<id>', views.sale_detail, name='sale_detail'),
	path('sales_on_standby', views.sales_on_standby, name='sales_on_standby'),
	path('SalesGroup_detail/<id>', views.SalesGroup_detail, name='SalesGroup_detail'),
	path('validated_SalesGroups/', views.validated_SalesGroups, name='validated_SalesGroups')
]