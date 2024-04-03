from django.contrib import admin
from django.urls import path

from . import views #Referencio al archivo views para usar sus funciones.

app_name = 'Accounts' #Aquí se le especifica a django el nombre de la app para que no se confunda con los otros archivos "urls.py"

urlpatterns = [
	path('', views.usersList, name="users"),
	path('signup/', views.signupView, name="signup"),
	path('login/', views.loginView, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('userProfile/<id>', views.userProfile, name="userProfile"),
	path('modifyMyProfile/', views.modifyMyProfile, name="modifyMyProfile"), #URL para que cada usuario pueda editar su propio perfil.



	path('deactivate_user_request/<id>', views.deactivate_user_request, name='deactivate_user_request'),
	path('unvalidated_DeactivateUser_Requests/', views.unvalidated_DeactivateUser_Requests, name='unvalidated_DeactivateUser_Requests'),
	path('validate_user_deactivation/<id>', views.validate_user_deactivation, name='validate_user_deactivation'),
	path('validated_DeactivateUser_Requests/', views.validated_DeactivateUser_Requests, name='validated_DeactivateUser_Requests'),
	path('DeactivateUser_detail/<id>', views.DeactivateUser_detail, name='DeactivateUser_detail'),


	path('inactive_users/', views.inactive_users, name='inactive_users'),
	path('restore_user_request/<id>', views.restore_user_request, name='restore_user_request'),
	path('unvalidated_RestoreUser_Requests/', views.unvalidated_RestoreUser_Requests, name='unvalidated_RestoreUser_Requests'),
	path('validate_user_restore/<id>', views.validate_user_restore, name='validate_user_restore'),
	path('validated_RestoreUser_Requests/', views.validated_RestoreUser_Requests, name='validated_RestoreUser_Requests'),
	path('RestoreUser_detail/<id>', views.RestoreUser_detail, name='RestoreUser_detail'),


	path('unvalidated_invitation_requests/', views.unvalidated_invitation_requests, name='unvalidated_invitation_requests'),
	path('validate_invitation/<id>', views.validate_invitation, name='validate_invitation'),
	path('validated_invitation_requests/', views.validated_invitation_requests, name='validated_invitation_requests'),
]
