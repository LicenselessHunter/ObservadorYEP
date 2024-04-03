from django.contrib import admin
from django.urls import path
from . import views #Referencio al archivo views para usar sus funciones.

app_name = 'tables'

urlpatterns = [

	path('', views.products, name='products'),
	path('unvalidated_products/', views.unvalidated_products, name='unvalidated_products'),
	path('validate_product/<id>', views.validate_product, name='validate_product'),
	path('Product_detail/<id>', views.Product_detail, name='Product_detail'),
	path('pack_creation/<int:child_number>', views.pack_creation, name='pack_creation'),

	path('unvalidated_ModifyProduct_Requests/', views.unvalidated_ModifyProduct_Requests, name='unvalidated_ModifyProduct_Requests'),
	path('modify_product_request/<id>', views.modify_product_request, name='modify_product_request'),
	path('validate_product_modification/<id>', views.validate_product_modification, name='validate_product_modification'),
	path('validated_ModifyProduct_Requests/', views.validated_ModifyProduct_Requests, name='validated_ModifyProduct_Requests'),
	path('ModifyProduct_detail/<id>', views.ModifyProduct_detail, name='ModifyProduct_detail'),

	path('unvalidated_DeactivateProduct_Requests/', views.unvalidated_DeactivateProduct_Requests, name='unvalidated_DeactivateProduct_Requests'),
	path('deactivate_product_request/<id>', views.deactivate_product_request, name='deactivate_product_request'),
	path('validate_product_deactivation/<id>', views.validate_product_deactivation, name='validate_product_deactivation'),
	path('validated_DeactivateProduct_Requests/', views.validated_DeactivateProduct_Requests, name='validated_DeactivateProduct_Requests'),
	path('DeactivateProduct_detail/<id>', views.DeactivateProduct_detail, name='DeactivateProduct_detail'),


	path('inactive_products/', views.inactive_products, name='inactive_products'),
	path('restore_product_request/<id>', views.restore_product_request, name='restore_product_request'),
	path('unvalidated_RestoreProduct_Requests/', views.unvalidated_RestoreProduct_Requests, name='unvalidated_RestoreProduct_Requests'),
	path('validate_product_restore/<id>', views.validate_product_restore, name='validate_product_restore'),
	path('validated_RestoreProduct_Requests/', views.validated_RestoreProduct_Requests, name='validated_RestoreProduct_Requests'),
	path('RestoreProduct_detail/<id>', views.RestoreProduct_detail, name='RestoreProduct_detail'),

]