from django.shortcuts import render, redirect
from .models import Marketplace, ModifyMarketplace_Request, DeactivationMarketplace_Request, RestoreMarketplace_Request
from . import forms
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required #Se importa el decorator.


# Create your views here.


#----------- CREATION VIEWS --------------

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def marketplaces(request):
	validated_marketplaces = Marketplace.objects.filter(STATE = 'Activo', validation = True).order_by('-validation_date') 


	if request.method == 'POST' and 'createMarketplace' in request.POST: #Si se está mandando el data escrito en el formulario.
		
		form = forms.MarketplaceForm(request.POST, request.FILES) #Nueva instancia form. Aqui vamos a pasar el "request" que tiene información acerca del request que fue hecho y .POST para acceder al data, toda la data que viene con el post request. Estamos pasando toda esta data a una nueva instancia del form.

		if form.is_valid():#Se usara el método "is_valid()" para correr una validación y retornar un booleano diciendo si el data es valido.
			marketplaceInstance = form.save(commit=False)
			marketplaceInstance.created_by = request.user #Se guarda el campo 'User_related' con el usuario actual, dejando regustro del usuario que creo el producto.


			marketplaceInstance = form.save() #Se guarda el registro en la base de datos

			messages.success(request, 'Canal creado con éxito, queda a espera de ser validado por un administrador')

			return redirect ("marketplaces:unvalidated_marketplaces")

		else:
			messages.error(request, 'Error en creación de canal, revisar formulario para más detalle')

	#FIN CREACIÓN DE PRODUCTO NO VALIDADO

	form = forms.MarketplaceForm() #Instancia de formulario vacío.

	context = {
		'validated_marketplaces':validated_marketplaces,
		'form':form,
	}

	return render(request, "marketplaces/marketplaces.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_marketplaces(request):
	unvalidated_marketplaces = Marketplace.objects.filter(STATE = 'Activo', validation = False).order_by('-id')


	context = {
		'unvalidated_marketplaces':unvalidated_marketplaces,
	}

	return render(request, "marketplaces/unvalidated_marketplaces.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_marketplace(request, id):
	marketplaceInstance = Marketplace.objects.get(id=id)


	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:unvalidated_products")


	#----- CONFIRMAR SI PRODUCTO YA ESTÁ VALIDADO --------
	if marketplaceInstance.validation == True:
		messages.error(request, 'No puedes revalidar un producto ya validado')
		return redirect ("marketplaces:unvalidated_products")


	if request.method == 'POST' and 'validateMarketplace' in request.POST:
		marketplaceInstance.validation = True
		marketplaceInstance.validation_by = request.user
		marketplaceInstance.validation_date = now()

		marketplaceInstance.save()

		messages.success(request, 'Canal validado con éxito')
		return redirect ("marketplaces:marketplaces")

	elif request.method == 'POST' and 'rejectMarketplace' in request.POST:
		marketplaceInstance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("marketplaces:unvalidated_marketplaces")

	context = {
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/validate_marketplace.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def Marketplace_detail(request, id):
	marketplaceInstance = Marketplace.objects.get(id = id)
	

	context = {
		'marketplace':marketplaceInstance,
	}


	return render(request, "marketplaces/Marketplaces_detail.html", context)




#----------- MODIFICATION VIEWS --------------


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_ModifyMarketplace_Requests(request):
	unvalidated_ModifyMarketplace_Requests = ModifyMarketplace_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_ModifyMarketplace_Requests':unvalidated_ModifyMarketplace_Requests,
	}

	return render(request, "marketplaces/unvalidated_ModifyMarketplace_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def modify_marketplace_request(request, id):
	marketplaceInstance = Marketplace.objects.get(id=id)


	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:marketplaces")

	#----- CONFIRMAR SI PRODUCTO YA FUE DESACTIVADO -----
	if marketplaceInstance.STATE == 'Inactivo':
		messages.error(request, 'No puedes modificar un canal de venta inactivo')
		return redirect ("marketplaces:marketplaces")


	#----- CONFIRMAR SI PRODUCTO NO ESTÁ VALIDADO --------
	if marketplaceInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("marketplaces:marketplaces")


	if request.method == 'POST' and 'modify_marketplace_request' in request.POST:
		Actual_referencial_description = marketplaceInstance.referencial_description
		Actual_marketplace_image = marketplaceInstance.marketplace_image

		

		form = forms.MarketplaceEditForm(request.POST, request.FILES, instance=marketplaceInstance)

		marketplaceInstance = form.save(commit=False)

		#---- EXCEOPCIÓN POR SI SE INTENTA MANDAR UNA MODIFICACIÓN CON EXACTAMENTE LOS MISMOS CAMPOS ACTUALES DEL ELEMENTO QUE SE QUIERE CAMBIAR  ------
		if Actual_referencial_description == marketplaceInstance.referencial_description and Actual_marketplace_image == marketplaceInstance.marketplace_image:

			messages.error(request, 'No puede crear una solicitud de modificación sin cambiar nada')
			return redirect ("marketplaces:marketplaces")

		if form.is_valid():

			#---- EXCEOPCIÓN POR SI YA EXISTE UNA SOLICITUD NO VALIDADA CON LOS CAMPOS QUE DESEA EL SOLICITANTE  ------
			if ModifyMarketplace_Request.objects.filter(id_marketplace = marketplaceInstance, modified_referencial_description = marketplaceInstance.referencial_description, modified_marketplace_image = marketplaceInstance.marketplace_image, validation = False).exists():

				ExistingRequest = ModifyMarketplace_Request.objects.get(id_marketplace = marketplaceInstance, modified_referencial_description = marketplaceInstance.referencial_description, modified_marketplace_image = marketplaceInstance.marketplace_image, validation = False)

				messages.error(request, 'La solicitud no validada de id ' + str(ExistingRequest.id) + ' ya contiene las modificaciones que desea')
				return redirect ("marketplaces:marketplaces")




			modifyMarketplace_request_instance = ModifyMarketplace_Request.objects.create(id_marketplace = marketplaceInstance, modified_referencial_description = marketplaceInstance.referencial_description, modified_marketplace_image = marketplaceInstance.marketplace_image, created_by = request.user, created_date = now())


			modifyMarketplace_request_instance.save()
			messages.success(request, 'Solicitud de modificación creada con éxito, queda a espera de ser validada por un administrador')
			return redirect ("marketplaces:unvalidated_ModifyMarketplace_Requests")

	else:
		form = forms.MarketplaceEditForm(instance=marketplaceInstance)


	context = {
		'form': form,
	}

	return render(request, "marketplaces/modify_marketplace_request.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_marketplace_modification(request, id):
	modifyMarketplace_request_instance = ModifyMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = modifyMarketplace_request_instance.id_marketplace.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:unvalidated_ModifyMarketplace_Requests")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if modifyMarketplace_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		#return redirect ("marketplaces:validated_ModifyMarketplace_Requests")


	if request.method == 'POST' and 'validateModification' in request.POST:
		modifyMarketplace_request_instance.past_referencial_description = marketplaceInstance.referencial_description
		modifyMarketplace_request_instance.past_marketplace_image = marketplaceInstance.marketplace_image


		modifyMarketplace_request_instance.validation_by = request.user
		modifyMarketplace_request_instance.validation_date = now()
		modifyMarketplace_request_instance.validation = True

		marketplaceInstance.referencial_description = modifyMarketplace_request_instance.modified_referencial_description
		marketplaceInstance.marketplace_image = modifyMarketplace_request_instance.modified_marketplace_image

		marketplaceInstance.save()
		modifyMarketplace_request_instance.save()

		messages.success(request, 'Canal de venta Modificado con éxito')
		return redirect ("marketplaces:marketplaces")

	elif request.method == 'POST' and 'rejectModification' in request.POST:
		modifyMarketplace_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("marketplaces:unvalidated_ModifyMarketplace_Requests")

	context = {
		'ModifyRequest':modifyMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/validate_marketplace_modification.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_ModifyMarketplace_Requests(request):

	validated_ModifyMarketplace_Requests = ModifyMarketplace_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_ModifyMarketplace_Requests':validated_ModifyMarketplace_Requests,
	}

	return render(request, "marketplaces/validated_ModifyMarketplace_Requests.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def ModifyMarketplace_detail(request, id):
	modifyMarketplace_request_instance = ModifyMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = modifyMarketplace_request_instance.id_marketplace.id)

	context = {
		'ModifyRequest':modifyMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/ModifyMarketplace_detail.html", context)



#----------- DEACTIVATION VIEWS --------------


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_DeactivateMarketplace_Requests(request):

	unvalidated_DeactivateMarketplace_Requests = DeactivationMarketplace_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_DeactivateMarketplace_Requests':unvalidated_DeactivateMarketplace_Requests,
	}

	return render(request, "marketplaces/unvalidated_DeactivateMarketplace_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def deactivate_marketplace_request(request, id):
	marketplaceInstance = Marketplace.objects.get(id=id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:marketplaces")

	#----- CONFIRMAR SI PRODUCTO YA FUE DESACTIVADO -----
	if marketplaceInstance.STATE == 'Inactivo':
		messages.error(request, 'Este canal de venta ya está inactivo')
		return redirect ("marketplaces:marketplaces")


	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE CANAL ------
	if DeactivationMarketplace_Request.objects.filter(id_marketplace = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de desactivación para este canal')
		return redirect ("marketplaces:marketplaces")


	#----- CONFIRMAR SI PRODUCTO NO ESTÁ VALIDADO --------
	if marketplaceInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("marketplaces:marketplaces")


	context = {
		'marketplace':marketplaceInstance,
	}

	if request.method == 'POST' and 'deactivate_marketplace_request' in request.POST:

		deactivateMarketplace_request_instance = DeactivationMarketplace_Request.objects.create(id_marketplace = marketplaceInstance, created_by = request.user, created_date = now())
		deactivateMarketplace_request_instance.save()

		messages.success(request, 'Solicitud de desactivación creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("marketplaces:unvalidated_DeactivateMarketplace_Requests")

	return render(request, "marketplaces/deactivate_marketplace_request.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_marketplace_deactivation(request, id):
	deactivateMarketplace_request_instance = DeactivationMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = deactivateMarketplace_request_instance.id_marketplace.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:unvalidated_DeactivateMarketplace_Requests")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if deactivateMarketplace_request_instance == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("marketplaces:unvalidated_DeactivateMarketplace_Requests")


	if request.method == 'POST' and 'validateDeactivation' in request.POST:
		marketplaceInstance.STATE = 'Inactivo'
		deactivateMarketplace_request_instance.validation_by = request.user
		deactivateMarketplace_request_instance.validation_date = now()
		deactivateMarketplace_request_instance.validation = True

		marketplaceInstance.save()
		deactivateMarketplace_request_instance.save()

		messages.success(request, 'Canal de venta desactivado con éxito')
		return redirect ("marketplaces:inactive_marketplaces")

	elif request.method == 'POST' and 'rejectDeactivation' in request.POST:
		deactivateMarketplace_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("marketplaces:unvalidated_DeactivateMarketplace_Requests")

	context = {
		'DeactivateRequest':deactivateMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/validate_marketplace_deactivation.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_DeactivateMarketplace_Requests(request):

	validated_DeactivateMarketplace_Requests = DeactivationMarketplace_Request.objects.filter(validation = True).order_by('-id')

	context = {
		'validated_DeactivateMarketplace_Requests':validated_DeactivateMarketplace_Requests,
	}

	return render(request, "marketplaces/validated_DeactivateMarketplace_Requests.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def DeactivateMarketplace_detail(request, id):
	
	deactivateMarketplace_request_instance = DeactivationMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = deactivateMarketplace_request_instance.id_marketplace.id)

	context = {
		'DeactivateRequest':deactivateMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/DeactivateMarketplace_detail.html", context)



#----------- RESTORATION VIEWS --------------

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def inactive_marketplaces(request):
	inactivated_marketplaces = Marketplace.objects.filter(STATE = 'Inactivo', validation = True).order_by('-validation_date')

	context = {
		'inactivated_marketplaces':inactivated_marketplaces,
	}

	return render(request, "marketplaces/inactive_marketplaces.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def restore_marketplace_request(request, id):
	marketplaceInstance = Marketplace.objects.get(id=id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:inactive_marketplaces")

	#----- CONFIRMAR SI MARKETPLACE YA FUE DESACTIVADO -----
	if marketplaceInstance.STATE == 'Activo':
		messages.error(request, 'Este canal de venta ya está activo')
		return redirect ("marketplaces:inactive_marketplaces")


	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE CANAL ------
	if DeactivationMarketplace_Request.objects.filter(id_marketplace = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de restauración para este canal')
		return redirect ("marketplaces:inactive_marketplaces")


	#----- CONFIRMAR SI MARKETPLACE NO ESTÁ VALIDADO --------
	if marketplaceInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("marketplaces:inactive_marketplaces")


	context = {
		'marketplace':marketplaceInstance,
	}

	if request.method == 'POST' and 'restore_marketplace_request' in request.POST:

		restoreMarketplace_request_instance = RestoreMarketplace_Request.objects.create(id_marketplace = marketplaceInstance, created_by = request.user, created_date = now())
		restoreMarketplace_request_instance.save()

		messages.success(request, 'Solicitud de restauración creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("marketplaces:unvalidated_RestoreMarketplace_Requests")

	return render(request, "marketplaces/restore_marketplace_request.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_RestoreMarketplace_Requests(request):

	unvalidated_RestoreMarketplace_Requests = RestoreMarketplace_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_RestoreMarketplace_Requests':unvalidated_RestoreMarketplace_Requests,
	}

	return render(request, "marketplaces/unvalidated_RestoreMarketplace_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_marketplace_restore(request, id):
	restoreMarketplace_request_instance = RestoreMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = restoreMarketplace_request_instance.id_marketplace.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("marketplaces:unvalidated_RestoreMarketplace_Requests")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if restoreMarketplace_request_instance == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("marketplaces:unvalidated_RestoreMarketplace_Requests")


	if request.method == 'POST' and 'validateRestore' in request.POST:
		marketplaceInstance.STATE = 'Activo'
		restoreMarketplace_request_instance.validation_by = request.user
		restoreMarketplace_request_instance.validation_date = now()
		restoreMarketplace_request_instance.validation = True

		marketplaceInstance.save()
		restoreMarketplace_request_instance.save()

		messages.success(request, 'Canal de venta restaurado con éxito')
		return redirect ("marketplaces:marketplaces")

	elif request.method == 'POST' and 'rejectRestore' in request.POST:
		restoreMarketplace_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("marketplaces:unvalidated_RestoreMarketplace_Requests")

	context = {
		'RestoreRequest':restoreMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/validate_marketplace_restore.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_RestoreMarketplace_Requests(request):

	validated_RestoreMarketplace_Requests = RestoreMarketplace_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_RestoreMarketplace_Requests':validated_RestoreMarketplace_Requests,
	}

	return render(request, "marketplaces/validated_RestoreMarketplace_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def RestoreMarketplace_detail(request, id):
	
	restoreMarketplace_request_instance = RestoreMarketplace_Request.objects.get(id=id)
	marketplaceInstance = Marketplace.objects.get(id = restoreMarketplace_request_instance.id_marketplace.id)

	context = {
		'RestoreRequest':restoreMarketplace_request_instance,
		'marketplace':marketplaceInstance,
	}

	return render(request, "marketplaces/RestoreMarketplace_detail.html", context)