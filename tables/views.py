from django.shortcuts import render, redirect
from .models import Product, ModifyProduct_Request, DeactivationProduct_Request, RestoreProduct_Request, PackRelation
from . import forms
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required #Se importa el decorator.
from django.forms import formset_factory #Se importan los formsets


# Create your views here.


#----------- CREATION VIEWS --------------

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def products(request):
	validated_products = Product.objects.filter(STATE = 'Activo', validation = True).order_by('-validation_date') 

	#CREACIÓN DE PRODUCTO NO VALIDADO
	if request.method == 'POST' and 'createProduct' in request.POST: #Si se está mandando el data escrito en el formulario.
		
		form = forms.ProductForm(request.POST, request.FILES) #Nueva instancia form. Aqui vamos a pasar el "request" que tiene información acerca del request que fue hecho y .POST para acceder al data, toda la data que viene con el post request. Estamos pasando toda esta data a una nueva instancia del form.

		if form.is_valid():#Se usara el método "is_valid()" para correr una validación y retornar un booleano diciendo si el data es valido.
			productInstance = form.save(commit=False)
			productInstance.created_by = request.user #Se guarda el campo 'User_related' con el usuario actual, dejando regustro del usuario que creo el producto.


			productInstance = form.save() #Se guarda el registro en la base de datos

			messages.success(request, 'Producto creado con éxito, queda a espera de ser validado por un administrador')

			return redirect ("tables:unvalidated_products")

		else:
			messages.error(request, 'Error en creación de producto, revisar formulario para más detalle')

	#FIN CREACIÓN DE PRODUCTO NO VALIDADO

	elif request.method == 'POST' and 'defineChildQuantity' in request.POST:
		childQuantity_input = request.POST.get('childQuantity')

		return redirect("tables:pack_creation", childQuantity_input)


	form = forms.ProductForm() #Instancia de formulario vacío.

	context = {
		'validated_products':validated_products,
		'form':form,
	}

	return render(request, "tables/products.html", context)



@login_required(login_url="Accounts:login")
def pack_creation(request, child_number):
	
	#------- CONFIRMACIÓN DE TIPO DE USUARIO -------
	if request.user.profile.user_Type == 'Administrador':

		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect("tables:products")


	My_Formset = formset_factory(forms.PACK_Form, extra=child_number)

	if request.method == 'POST' and 'ConfirmButton' in request.POST:
		Pack_Formset = My_Formset(request.POST)
		Product_Form = forms.ProductForm(request.POST)

		if Pack_Formset.is_valid() and Product_Form.is_valid():
			ParentInstance = Product_Form.save(commit=False)
			ParentInstance.created_by = request.user
			ParentInstance.Product_type = 'PACK'

			ParentInstance.save()

			for form in Pack_Formset:
				ChildInstance = form.save(commit=False)

				if ChildInstance.CHILD_QUANTITY == 0:
					messages.error(request, 'La cantidad de un producto singular no puede ser 0')
					ParentInstance.delete()
					return redirect("tables:products")

				if child_number == 1 and ChildInstance.CHILD_QUANTITY <= 1:
					ParentInstance.delete()
					messages.error(request, 'Un pack debe tener por lo menos: un producto singular con 2 o más cantidades o dos productos singulares diferentes con cantidad 1')
					return redirect("tables:products")

				ChildInstance.SKU_PACK = ParentInstance
				Queryset = PackRelation.objects.filter(SKU_PACK = ChildInstance.SKU_PACK, SKU_CHILD=ChildInstance.SKU_CHILD)

				if Queryset.exists():
					ParentInstance.delete()
					messages.error(request, 'No se pueden tener 2 o más productos singulares iguales en un mismo PACK')
					return redirect("tables:products")

				ChildInstance.save()

			messages.success(request, 'Pack creado exitosamente, queda a espera de ser validado por un administrador')
			return redirect ("tables:unvalidated_products")


	else:
		Pack_Formset = My_Formset()
		Product_Form = forms.ProductForm()

	context = {
		'Pack_Formset':Pack_Formset,
		'Product_Form':Product_Form,
	}

	return render(request, "tables/pack_creation.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_products(request):
	unvalidated_products = Product.objects.filter(STATE = 'Activo', validation = False).order_by('-id')


	context = {
		'unvalidated_products':unvalidated_products,
	}

	return render(request, "tables/unvalidated_products.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_product(request, id):
	productInstance = Product.objects.get(id=id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:unvalidated_products")


	#----- CONFIRMAR SI PRODUCTO YA ESTÁ VALIDADO --------
	if productInstance.validation == True:
		messages.error(request, 'No puedes revalidar un producto ya validado')
		return redirect ("tables:unvalidated_products")


	if request.method == 'POST' and 'validateProduct' in request.POST:
		productInstance.validation = True
		productInstance.validation_by = request.user
		productInstance.validation_date = now()

		productInstance.save()

		messages.success(request, 'Producto validado con éxito')
		return redirect ("tables:products")

	elif request.method == 'POST' and 'rejectProduct' in request.POST:
		productInstance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("tables:unvalidated_products")

	context = {
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	return render(request, "tables/validate_product.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def Product_detail(request, id):
	productInstance = Product.objects.get(id = id)
	
	if productInstance.Product_type == 'PACK':
		PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

		context = {
			'product':productInstance,
			'PACKInformation':PACKInformation,
		}


	else:

		context = {
			'product':productInstance,
		}
	

	return render(request, "tables/Product_detail.html", context)







#----------- MODIFICATION VIEWS --------------

@login_required(login_url="Accounts:login")
def unvalidated_ModifyProduct_Requests(request):
	unvalidated_ModifyProduct_Requests = ModifyProduct_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_ModifyProduct_Requests':unvalidated_ModifyProduct_Requests,
	}

	return render(request, "tables/unvalidated_ModifyProduct_Requests.html", context)


@login_required(login_url="Accounts:login")
def unvalidated_ModifyProduct_detail(request, id):
	modifyProduct_request_instance = ModifyProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = modifyProduct_request_instance.id_product.id)	



@login_required(login_url="Accounts:login")
def modify_product_request(request, id):
	productInstance = Product.objects.get(id=id)


	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:products")

	#----- CONFIRMAR SI PRODUCTO YA FUE DESACTIVADO -----
	if productInstance.STATE == 'Inactivo':
		messages.error(request, 'No puedes modificar un producto inactivo')
		return redirect ("tables:products")


	#----- CONFIRMAR SI PRODUCTO NO ESTÁ VALIDADO --------
	if productInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("tables:products")


	if request.method == 'POST' and 'modify_product_request' in request.POST:
		Actual_description = productInstance.Description
		Actual_product_image = productInstance.product_image
		Actual_classification = productInstance.classification

		#modifyProduct_request_instance = ModifyProduct_Request.objects.create(id_product = productInstance, created_by = request.user, created_date = now())
		form = forms.ProductEditForm(request.POST, request.FILES, instance=productInstance)

		productInstance = form.save(commit=False)
		if Actual_description == productInstance.Description and Actual_product_image == productInstance.product_image and Actual_classification == productInstance.classification:

			messages.error(request, 'No puede crear una solicitud de modificación sin cambiar nada')
			return redirect ("tables:products")

		if form.is_valid():

			#---- EXCEOPCIÓN POR SI YA EXISTE UNA SOLICITUD NO VALIDADA CON LOS CAMPOS QUE DESEA EL SOLICITANTE  ------
			if ModifyProduct_Request.objects.filter(id_product = productInstance, modified_Description = productInstance.Description, modified_classification = productInstance.classification, modified_product_image = productInstance.product_image, validation = False).exists():

				ExistingRequest = ModifyProduct_Request.objects.get(id_product = productInstance, modified_Description = productInstance.Description, modified_classification = productInstance.classification, modified_product_image = productInstance.product_image, validation = False)

				messages.error(request, 'La solicitud no validada de id ' + str(ExistingRequest.id) + ' ya contiene las modificaciones que desea')
				return redirect ("tables:products")


					

			modifyProduct_request_instance = ModifyProduct_Request.objects.create(id_product = productInstance, modified_Description = productInstance.Description, modified_classification = productInstance.classification, modified_product_image = productInstance.product_image,  created_by = request.user, created_date = now())


			modifyProduct_request_instance.save()
			messages.success(request, 'Solicitud de modificación creada con éxito, queda a espera de ser validada por un administrador')
			return redirect ("tables:unvalidated_ModifyProduct_Requests")

	else:
		form = forms.ProductEditForm(instance=productInstance)


	context = {
		'form': form,
	}

	return render(request, "tables/modify_product_request.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_product_modification(request, id):
	modifyProduct_request_instance = ModifyProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = modifyProduct_request_instance.id_product.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:unvalidated_products")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if modifyProduct_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("tables:unvalidated_products")


	if request.method == 'POST' and 'validateModification' in request.POST:
		modifyProduct_request_instance.past_Description = productInstance.Description
		modifyProduct_request_instance.past_classification = productInstance.classification
		modifyProduct_request_instance.past_product_image = productInstance.product_image

		modifyProduct_request_instance.validation_by = request.user
		modifyProduct_request_instance.validation_date = now()
		modifyProduct_request_instance.validation = True

		productInstance.Description = modifyProduct_request_instance.modified_Description
		productInstance.classification = modifyProduct_request_instance.modified_classification
		productInstance.product_image = modifyProduct_request_instance.modified_product_image

		productInstance.save()
		modifyProduct_request_instance.save()

		messages.success(request, 'Producto Modificado con éxito')
		return redirect ("tables:products")

	elif request.method == 'POST' and 'rejectModification' in request.POST:
		modifyProduct_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("tables:unvalidated_ModifyProduct_Requests")

	context = {
		'ModifyRequest':modifyProduct_request_instance,
		'product':productInstance,
	}

	return render(request, "tables/validate_product_modification.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_ModifyProduct_Requests(request):

	validated_ModifyProduct_Requests = ModifyProduct_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_ModifyProduct_Requests':validated_ModifyProduct_Requests,
	}

	return render(request, "tables/validated_ModifyProduct_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def ModifyProduct_detail(request, id):
	modifyProduct_request_instance = ModifyProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = modifyProduct_request_instance.id_product.id)

	context = {
		'ModifyRequest':modifyProduct_request_instance,
		'product':productInstance,
	}

	return render(request, "tables/ModifyProduct_detail.html", context)








#----------- DEACTIVATION VIEWS --------------


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_DeactivateProduct_Requests(request):

	unvalidated_DeactivateProduct_Requests = DeactivationProduct_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_DeactivateProduct_Requests':unvalidated_DeactivateProduct_Requests,
	}

	return render(request, "tables/unvalidated_DeactivateProduct_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def deactivate_product_request(request, id):
	productInstance = Product.objects.get(id=id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:products")

	#----- CONFIRMAR SI PRODUCTO YA FUE DESACTIVADO -----
	if productInstance.STATE == 'Inactivo':
		messages.error(request, 'Este producto ya está inactivo')
		return redirect ("tables:products")


	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE PRODUCTO ------
	if DeactivationProduct_Request.objects.filter(id_product = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de desactivación para este producto')
		return redirect ("tables:products")


	#----- CONFIRMAR SI PRODUCTO NO ESTÁ VALIDADO --------
	if productInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("tables:products")


	context = {
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	if request.method == 'POST' and 'deactivate_product_request' in request.POST:

		deactivateProduct_request_instance = DeactivationProduct_Request.objects.create(id_product = productInstance, created_by = request.user, created_date = now())
		deactivateProduct_request_instance.save()

		messages.success(request, 'Solicitud de desactivación creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("tables:unvalidated_DeactivateProduct_Requests")

	return render(request, "tables/deactivate_product_request.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_product_deactivation(request, id):
	deactivateProduct_request_instance = DeactivationProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = deactivateProduct_request_instance.id_product.id)
	RelatedPACKS = PackRelation.objects.filter(SKU_CHILD = productInstance, SKU_PACK__STATE = 'Activo')
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:unvalidated_DeactivateProduct_Requests")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if deactivateProduct_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("tables:unvalidated_DeactivateProduct_Requests")


	if request.method == 'POST' and 'validateDeactivation' in request.POST:
		productInstance.STATE = 'Inactivo'
		deactivateProduct_request_instance.validation_by = request.user
		deactivateProduct_request_instance.validation_date = now()
		deactivateProduct_request_instance.validation = True

		productInstance.save()
		deactivateProduct_request_instance.save()


		if RelatedPACKS.exists(): #Si es que productInstance es Singular y está asociado a packs.
			for obj in RelatedPACKS:
				PackInstance = Product.objects.get(SKU = obj.SKU_PACK)
				PackInstance.STATE = 'Inactivo' #este producto sera eliminado.

				PackInstance.save()


		messages.success(request, 'Producto desactivado con éxito')
		return redirect ("tables:inactive_products")

	elif request.method == 'POST' and 'rejectDeactivation' in request.POST:
		deactivateProduct_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("tables:unvalidated_DeactivateProduct_Requests")

	context = {
		'RelatedPACKS':RelatedPACKS,
		'DeactivateRequest':deactivateProduct_request_instance,
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	return render(request, "tables/validate_product_deactivation.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def inactive_products(request):
	inactivated_products = Product.objects.filter(STATE = 'Inactivo', validation = True).order_by('-validation_date')

	context = {
		'inactivated_products':inactivated_products,
	}

	return render(request, "tables/inactive_products.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_DeactivateProduct_Requests(request):

	validated_DeactivateProduct_Requests = DeactivationProduct_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_DeactivateProduct_Requests':validated_DeactivateProduct_Requests,
	}

	return render(request, "tables/validated_DeactivateProduct_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def DeactivateProduct_detail(request, id):
	deactivateProduct_request_instance = DeactivationProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = deactivateProduct_request_instance.id_product.id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	context = {
		'DeactivateRequest':deactivateProduct_request_instance,
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	return render(request, "tables/DeactivateProduct_detail.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def restore_product_request(request, id):
	productInstance = Product.objects.get(id=id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)
	

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:inactive_products")

	#----- CONFIRMAR SI PRODUCTO YA FUE RESTAURADO -----
	if productInstance.STATE == 'Activo':
		messages.error(request, 'El producto que intenta restaurar ya está activo')
		return redirect ("tables:inactive_products")


	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE PRODUCTO ------
	if RestoreProduct_Request.objects.filter(id_product = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de restauración para este producto')
		return redirect ("tables:inactive_products")

	#----- CONFIRMAR SI PRODUCTO NO ESTÁ VALIDADO --------
	if productInstance.validation == False:
		messages.error(request, 'No puedes Hacer eso')
		return redirect ("tables:inactive_products")

	#------- EVITAR QUE UN PACK SE PUEDA RESTAURAR SI ALGUNO DE SUS PRODUCTOS SINGULARES ESTÁ INACTIVO -------
	if productInstance.Product_type == 'PACK':
		QuerySet = PackRelation.objects.filter(SKU_PACK = productInstance)

		for Obj in QuerySet:
			SingularProductInstance = Product.objects.get(SKU = Obj.SKU_CHILD)

			if SingularProductInstance.STATE == 'Inactivo':
				messages.error(request, 'No puedes solicitar restaurar un pack si alguno de sus productos singulares está inactivo')
				return redirect ("tables:inactive_products")


	context = {
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	if request.method == 'POST' and 'restore_product_request' in request.POST:

		restoreProduct_request_instance = RestoreProduct_Request.objects.create(id_product = productInstance, created_by = request.user, created_date = now())
		restoreProduct_request_instance.save()

		messages.success(request, 'Solicitud de restauración de producto creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("tables:unvalidated_RestoreProduct_Requests")
		
	return render(request, "tables/restore_product_request.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_RestoreProduct_Requests(request):

	unvalidated_RestoreProduct_Requests = RestoreProduct_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_RestoreProduct_Requests':unvalidated_RestoreProduct_Requests,
	}

	return render(request, "tables/unvalidated_RestoreProduct_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_product_restore(request, id):
	restoreProduct_request_instance = RestoreProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = restoreProduct_request_instance.id_product.id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("tables:unvalidated_RestoreProduct_Requests")


	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if restoreProduct_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("tables:unvalidated_RestoreProduct_Requests")

	#------- EVITAR QUE UN PACK SE PUEDA RESTAURAR SI ALGUNO DE SUS PRODUCTOS SINGULARES ESTÁ INACTIVO -------
	if productInstance.Product_type == 'PACK':
		QuerySet = PackRelation.objects.filter(SKU_PACK = productInstance)

		for Obj in QuerySet:
			SingularProductInstance = Product.objects.get(SKU = Obj.SKU_CHILD)

			if SingularProductInstance.STATE == 'Inactivo':
				messages.error(request, 'No puedes restaurar un pack si alguno de sus productos singulares está inactivo')
				return redirect ("tables:unvalidated_RestoreProduct_Requests")



	if request.method == 'POST' and 'validateRestore' in request.POST:
		productInstance.STATE = 'Activo'
		restoreProduct_request_instance.validation_by = request.user
		restoreProduct_request_instance.validation_date = now()
		restoreProduct_request_instance.validation = True

		productInstance.save()
		restoreProduct_request_instance.save()

		messages.success(request, 'Producto restaurado con éxito')
		return redirect ("tables:products")

	elif request.method == 'POST' and 'rejectRestore' in request.POST:
		restoreProduct_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("tables:unvalidated_RestoreProduct_Requests")

	context = {
		'product':productInstance,
		'RestoreRequest':restoreProduct_request_instance,
		'PACKInformation':PACKInformation,
	}

	return render(request, "tables/validate_product_restore.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_RestoreProduct_Requests(request):

	validated_RestoreProduct_Requests = RestoreProduct_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_RestoreProduct_Requests':validated_RestoreProduct_Requests,
	}

	return render(request, "tables/validated_RestoreProduct_Requests.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def RestoreProduct_detail(request, id):
	restorationProduct_request_instance = RestoreProduct_Request.objects.get(id=id)
	productInstance = Product.objects.get(id = restorationProduct_request_instance.id_product.id)
	PACKInformation = PackRelation.objects.filter(SKU_PACK = productInstance)

	context = {
		'RestoreRequest':restorationProduct_request_instance,
		'product':productInstance,
		'PACKInformation':PACKInformation,
	}

	return render(request, "tables/RestoreProduct_detail.html", context)