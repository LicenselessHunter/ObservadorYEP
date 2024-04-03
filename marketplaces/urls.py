from django.contrib import admin
from django.urls import path
from . import views

app_name = 'marketplaces'

urlpatterns = [
	path('', views.marketplaces, name='marketplaces'),
	path('unvalidated_marketplaces/', views.unvalidated_marketplaces, name='unvalidated_marketplaces'),
	path('validate_marketplace/<id>', views.validate_marketplace, name='validate_marketplace'),
	path('Marketplace_detail/<id>', views.Marketplace_detail, name='Marketplace_detail'),

	path('unvalidated_ModifyMarketplace_Requests/', views.unvalidated_ModifyMarketplace_Requests, name='unvalidated_ModifyMarketplace_Requests'),
	path('modify_marketplace_request/<id>', views.modify_marketplace_request, name='modify_marketplace_request'),
	path('validate_marketplace_modification/<id>', views.validate_marketplace_modification, name='validate_marketplace_modification'),
	path('validated_ModifyMarketplace_Requests/', views.validated_ModifyMarketplace_Requests, name='validated_ModifyMarketplace_Requests'),
	path('DeactivateMarketplace_detail/<id>', views.DeactivateMarketplace_detail, name='DeactivateMarketplace_detail'),
	path('ModifyMarketplace_detail/<id>', views.ModifyMarketplace_detail, name='ModifyMarketplace_detail'),


	path('unvalidated_DeactivateMarketplace_Requests/', views.unvalidated_DeactivateMarketplace_Requests, name='unvalidated_DeactivateMarketplace_Requests'),
	path('deactivate_marketplace_request/<id>', views.deactivate_marketplace_request, name='deactivate_marketplace_request'),
	path('validate_marketplace_deactivation/<id>', views.validate_marketplace_deactivation, name='validate_marketplace_deactivation'),
	path('validated_DeactivateMarketplace_Requests/', views.validated_DeactivateMarketplace_Requests, name='validated_DeactivateMarketplace_Requests'),
	path('DeactivateMarketplace_detail/<id>', views.DeactivateMarketplace_detail, name='DeactivateMarketplace_detail'),

	path('inactive_marketplaces/', views.inactive_marketplaces, name='inactive_marketplaces'),
	path('restore_marketplace_request/<id>', views.restore_marketplace_request, name='restore_marketplace_request'),
	path('unvalidated_RestoreMarketplace_Requests/', views.unvalidated_RestoreMarketplace_Requests, name='unvalidated_RestoreMarketplace_Requests'),
	path('validate_marketplace_restore/<id>', views.validate_marketplace_restore, name='validate_marketplace_restore'),
	path('validated_RestoreMarketplace_Requests/', views.validated_RestoreMarketplace_Requests, name='validated_RestoreMarketplace_Requests'),
	path('RestoreMarketplace_detail/<id>', views.RestoreMarketplace_detail, name='RestoreMarketplace_detail'),

]