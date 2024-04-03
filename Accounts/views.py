from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm #Se importa form del login y registro.
from django.contrib.auth import login, logout #Usaremos la función "login" para logear al usuario. Se usara función "logout" para cerrar logeo de usuario.
from .models import Profile, DeactivationUser_Request, RestoreUser_Request, Invitation
from django.contrib.auth.models import User #Se importa el model User que esta implicito en Django.
from django.contrib.auth.decorators import login_required #Se importa el decorator.
from django.contrib import messages
from django.utils.timezone import now
from .forms import InvitationForm, Invitation_SignUpForm, MyUserUpdateForm, MyProfileUpdateForm

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 
from django.template.loader import render_to_string

import random

def signupView(request):
	if request.method == 'POST': #Si es un post request va a equivaler a un 'POST'.
		signUpform = UserCreationForm(request.POST) #Nueva instancia form. Aqui vamos a pasar el "request" que tiene información acerca del request que fue hecho y .POST para acceder al data, toda la data que viene con el post request. Estamos pasando toda esta data a una nueva instancia del form. Lo que estaría haciendo esto es validarlo por nosotros. Es el nombre correcto? las contraseñas coinciden?, etc...
		invite_SignUpForm = Invitation_SignUpForm(request.POST)

		if signUpform.is_valid() and invite_SignUpForm.is_valid(): #Se usara el método "is_valid()" para correr una validación y retornar un booleano diciendo si el data es valido.
			userObj = signUpform.save(commit=False) 
			inviteObj = invite_SignUpForm.save(commit=False)

			try: #Se probara este código, se parara si es que encuentra alguna excepción.
				inviteQueryInstance = Invitation.objects.get(email = inviteObj.email, code = inviteObj.code) #'inviteQueryInstance' representa al objeto del model  'Invitation' en donde el email y código es igual al puesto en el form de registro.

				userObj.email = inviteObj.email
				userObj.save()

				profileObj = Profile.objects.create(user = userObj, user_Type = inviteQueryInstance.user_Type)
				profileObj.save()

			except: #Si es que se encuentra alguna excepción.
				messages.error(request, 'El email y/o código es incorrecto')

			else: #Lo que pasa después si es que no ocurre ninguna excepción en el try.

				login(request, userObj) #Se logea en sistema el usuario recién creado.

				return redirect('home') #Se redirecciona al nuevo usuario a la página principal.
	
	else:  #Si es un get request.
		signUpform = UserCreationForm() #Instancia del "Form"
		invite_SignUpForm = Invitation_SignUpForm()

	context = {
		'signUpform':signUpform,
		'invite_SignUpForm':invite_SignUpForm,
	}

	return render(request, 'Accounts/signUp.html', context)

def loginView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST) #Instancia del "Form". Se hace lo mismo que en el de signup para validar, pero esta vez hay que especificar que es data con "data=" ya que no es el primer parametro que se espera de esta instancia en particular.
		if form.is_valid():
			user = form.get_user() #user va a ser igual al usuario que se escribio en el login form y aprobo la autentificación. Eso se obtiene con "get_user()" función propia de django.
			login(request, user) #Se va a usar la función importada "login" que le mandaremos como parametros una request para que loge al usuario contenido en "user".
			return redirect('home')

	else:
		form = AuthenticationForm() #Instancia del form.
	return render(request, 'Accounts/login.html', {'form':form}) #Se va a mostrar este template en el front-end
											 #Diccionario con data (que en este caso es la variable "form") que va a ser mandada al template "login"

def logout_view(request):
	logout(request) 
	return redirect('Accounts:login') 


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def usersList(request):
	activeProfiles = Profile.objects.filter(user__is_active = True)


	if request.method == 'POST':

		form = InvitationForm(request.POST)

		if form.is_valid():
			invitationObj = form.save(commit=False)

			if Invitation.objects.filter(email = invitationObj.email).exists():
				messages.error(request, 'Ya se ha mandado invitación a esta dirección de correo')

				return redirect("Accounts:users")

			VerifyCodeGeneration(invitationObj)

			invitationObj.User_sender = request.user #El campo que muestra el usuario emisor, se igualara al usuario actual.

			invitationObj.save()
			messages.success(request, 'Invitación enviada exitosamente, queda a espera de ser validada por un administrador')
			return redirect('Accounts:unvalidated_invitation_requests')

	else:
		form = InvitationForm()


	context = {
		'form':form,
		'activeProfiles':activeProfiles,
	}

	return render(request, 'Accounts/usersList.html', context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def userProfile(request, id):
	profileInstance = Profile.objects.get(id=id)

	return render(request, "Accounts/userProfile.html", {'profile':profileInstance})

#Función para que cada usuario pueda actualizar su propio perfil.
@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def modifyMyProfile(request):
    userInstance = request.user #'request.user' representa al actual usuario.
    profileInstance = request.user.profile

    if request.method == 'POST' and 'ConfirmButton' in request.POST:
        MyUserForm = MyUserUpdateForm(request.POST, instance = userInstance)
        MyProfileForm = MyProfileUpdateForm(request.POST, request.FILES, instance = profileInstance)
        #El 'request.FILES', es que se estan pasando archivos, en este caso, laimágen de perfil.
        if MyUserForm.is_valid() and MyProfileForm.is_valid():
            MyUserForm.save()
            MyProfileForm.save()

            messages.success(request, 'Su perfil ha sido editado exitosamente')
            return redirect("Accounts:users")


    else:
        MyUserForm = MyUserUpdateForm(instance = userInstance)
        MyProfileForm = MyProfileUpdateForm(instance = profileInstance)

    context = {
        'MyUserForm':MyUserForm,
        'MyProfileForm':MyProfileForm,
    }

    return render(request, "Accounts/modifyMyProfile.html", context)



def VerifyCodeGeneration(invitationObj):
	usedCode = True
	
	while usedCode == True:
		invitationObj.code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for i in range(6))

		if Invitation.objects.filter(code = invitationObj.code).exists():
			pass
		
		else:
			usedCode = False      

	return


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_invitation_requests(request):

	unvalidated_invitation_requests = Invitation.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_invitation_requests':unvalidated_invitation_requests,
	}

	return render(request, "Accounts/unvalidated_invitation_requests.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_invitation(request, id):

	invitationObj = Invitation.objects.get(id = id)

	#--- EXCEPCIÓN POR SI USUARIO ES TRABAJADOR ----
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("Accounts:unvalidated_invitation_requests")

	#---- Si se intenta hacer la operación con una invitación ya validada -----
	if invitationObj.validation == True:
		messages.error(request, 'Esta invitación ya fue validada y enviada')
		return redirect ("Accounts:unvalidated_invitation_requests")

	if request.method == 'POST' and 'validateInvitation' in request.POST:

		invitationObj.validation = True
		invitationObj.validation_by = request.user
		invitationObj.validation_date = now()

		acceptation_url = settings.ACCEPTATION_URL


		content = render_to_string('Accounts/correo.html', {'code': invitationObj.code, 'acceptation_url': acceptation_url}) #render_to_string(template_name, context=None, request=None, using=None). render_to_string() loads a template like get_template() and calls its render() method immediately. Puede tomar argumentos: render_to_string(template_name, context=None, request=None, using=None)

		email = EmailMultiAlternatives('Invitación a observador YEP', '???', settings.EMAIL_HOST_USER, [invitationObj.email]) #(subject, contenido alternativo por si el principal falla, email que envía el mensaje, mail que recibira el mensaje.)
		email.attach_alternative(content, "text/html") #Se attachea el contenido del mensaje y su formato.
		email.send() #Se envía el mensaje

		messages.success(request, 'Invitación enviada y validada exitosamente')
		invitationObj.save()
		return redirect("Accounts:users")

	elif request.method == 'POST' and 'rejectInvitation' in request.POST:

		invitationObj.delete()

		messages.success(request, 'Invitación rechazada con éxito')
		return redirect ("Accounts:unvalidated_invitation_requests")


	context = {
		'invitation':invitationObj,
	}

	return render(request, 'Accounts/validate_invitation.html', context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_invitation_requests(request):
	validated_invitation_requests = Invitation.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_invitation_requests':validated_invitation_requests,
	}

	return render(request, "Accounts/validated_invitation_requests.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def inactive_users(request):
	inactiveProfiles = Profile.objects.filter(user__is_active = False)

	context = {
		'inactiveProfiles':inactiveProfiles,
	}

	return render(request, 'Accounts/inactive_users.html', context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def deactivate_user_request(request, id):
	userInstance = User.objects.get(id=id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("Accounts:users")

	#----- EXCEPCIÓN POR SI EL USUARIO QUE SE QUIERE DESACTIVAR ES EL MISMO USUARIO ACTUAL -----
	if request.user == userInstance:
		messages.error(request, 'No puedes hacer eso')
		return redirect ("Accounts:users")


	#----- CONFIRMAR SI USUARIO YA FUE DESACTIVADO -----
	if userInstance.is_active == False:
		messages.error(request, 'Este usuario ya está inactivo')
		return redirect ("Accounts:users")

	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE USUARIO ------
	if DeactivationUser_Request.objects.filter(id_user = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de desactivación para este usuario')
		return redirect ("Accounts:users")




	context = {
		'user':userInstance,
	}


	if request.method == 'POST' and 'deactivate_user_request' in request.POST:

		deactivateUser_request_instance = DeactivationUser_Request.objects.create(id_user = userInstance, created_by = request.user, created_date = now())
		deactivateUser_request_instance.save()

		messages.success(request, 'Solicitud de desactivación creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("Accounts:unvalidated_DeactivateUser_Requests")


	return render(request, 'Accounts/deactivate_user_request.html', context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_DeactivateUser_Requests(request):

	unvalidated_DeactivateUser_Requests = DeactivationUser_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_DeactivateUser_Requests':unvalidated_DeactivateUser_Requests,
	}

	return render(request, "Accounts/unvalidated_DeactivateUser_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_user_deactivation(request, id):
	deactivateUser_request_instance = DeactivationUser_Request.objects.get(id=id)
	userInstance = User.objects.get(id = deactivateUser_request_instance.id_user.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("Accounts:unvalidated_DeactivateUser_Requests")

	#----- EXCEPCIÓN POR SI EL USUARIO QUE SE QUIERE DESACTIVAR ES EL MISMO USUARIO ACTUAL -----
	if request.user == userInstance:
		messages.error(request, 'No puedes hacer eso')
		return redirect ("Accounts:unvalidated_DeactivateUser_Requests")

	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if deactivateUser_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("Accounts:unvalidated_DeactivateUser_Requests")


	if request.method == 'POST' and 'validateDeactivation' in request.POST:
		userInstance.is_active = False
		deactivateUser_request_instance.validation_by = request.user
		deactivateUser_request_instance.validation_date = now()
		deactivateUser_request_instance.validation = True

		userInstance.save()
		deactivateUser_request_instance.save()

		messages.success(request, 'Usuario desactivado con éxito')
		return redirect ("Accounts:inactive_users")

	elif request.method == 'POST' and 'rejectDeactivation' in request.POST:
		deactivateUser_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("Accounts:unvalidated_DeactivateUser_Requests")

	context = {
		'DeactivateRequest':deactivateUser_request_instance,
		'user':userInstance,
	}

	return render(request, "Accounts/validate_user_deactivation.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_DeactivateUser_Requests(request):

	validated_DeactivateUser_Requests = DeactivationUser_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_DeactivateUser_Requests':validated_DeactivateUser_Requests,
	}

	return render(request, "Accounts/validated_DeactivateUser_Requests.html", context)


@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def DeactivateUser_detail(request, id):
	
	deactivateUser_request_instance = DeactivationUser_Request.objects.get(id=id)
	userInstance = User.objects.get(id = deactivateUser_request_instance.id_user.id)

	context = {
		'DeactivateRequest':deactivateUser_request_instance,
		'user':userInstance,
	}

	return render(request, "Accounts/DeactivateUser_detail.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def restore_user_request(request, id):
	userInstance = User.objects.get(id=id)
	

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Administrador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("Accounts:inactive_users")


	#----- CONFIRMAR SI USUARIO ESTA ACTIVO -----
	if userInstance.is_active == True:
		messages.error(request, 'Este usuario está activo')
		return redirect ("Accounts:inactive_users")

	#----- SI YA EXISTE UNA SOLICITUD PARA ESTE USUARIO ------
	if RestoreUser_Request.objects.filter(id_user = id, validation = False).exists():
		messages.error(request, 'Ya existe una solicitud de restauración para este usuario')
		return redirect ("Accounts:inactive_users")


	context = {
		'user':userInstance,
	}

	if request.method == 'POST' and 'restore_user_request' in request.POST:

		restoreUser_request_instance = RestoreUser_Request.objects.create(id_user = userInstance, created_by = request.user, created_date = now())
		restoreUser_request_instance.save()

		messages.success(request, 'Solicitud de restauración creada con éxito, queda a espera de ser validada por un administrador')
		return redirect ("Accounts:unvalidated_RestoreUser_Requests")


	return render(request, 'Accounts/restore_user_request.html', context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def unvalidated_RestoreUser_Requests(request):

	unvalidated_RestoreUser_Requests = RestoreUser_Request.objects.filter(validation = False).order_by('-id')

	context = {
		'unvalidated_RestoreUser_Requests':unvalidated_RestoreUser_Requests,
	}

	return render(request, "Accounts/unvalidated_RestoreUser_Requests.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validate_user_restore(request, id):
	restoreUser_request_instance = RestoreUser_Request.objects.get(id=id)
	userInstance = User.objects.get(id = restoreUser_request_instance.id_user.id)

	#----- CONFIRMACIÓN DE TIPO DE USUARIO --------
	if request.user.profile.user_Type == 'Trabajador':
		messages.error(request, 'No tienes permiso para usar esa funcionalidad')
		return redirect ("Accounts:unvalidated_RestoreUser_Requests")

	#----- EXCEPCIÓN POR SI EL USUARIO QUE SE QUIERE DESACTIVAR ES EL MISMO USUARIO ACTUAL -----
	if request.user == userInstance:
		messages.error(request, 'No puedes hacer eso')
		return redirect ("Accounts:unvalidated_RestoreUser_Requests")

	#----- CONFIRMACIÓN SI SOLICITUD YA FUE VALIDADA --------
	if restoreUser_request_instance.validation == True:
		messages.error(request, 'La Solicitud a la que intentas ingresar ya fue validada')
		return redirect ("Accounts:unvalidated_RestoreUser_Requests")


	if request.method == 'POST' and 'validateRestore' in request.POST:
		userInstance.is_active = True
		restoreUser_request_instance.validation_by = request.user
		restoreUser_request_instance.validation_date = now()
		restoreUser_request_instance.validation = True

		userInstance.save()
		restoreUser_request_instance.save()

		messages.success(request, 'Usuario restaurado con éxito')
		return redirect ("Accounts:users")

	elif request.method == 'POST' and 'rejectRestore' in request.POST:
		restoreUser_request_instance.delete()

		messages.success(request, 'Solicitud rechazada con éxito')
		return redirect ("Accounts:unvalidated_RestoreUser_Requests")

	context = {
		'RestoreRequest':restoreUser_request_instance,
		'user':userInstance,
	}

	return render(request, "Accounts/validate_user_restore.html", context)



@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def validated_RestoreUser_Requests(request):
	validated_RestoreUser_Requests = RestoreUser_Request.objects.filter(validation = True).order_by('-validation_date')

	context = {
		'validated_RestoreUser_Requests':validated_RestoreUser_Requests,
	}

	return render(request, "Accounts/validated_RestoreUser_Requests.html", context)

@login_required(login_url="Accounts:login") #Decorator. Este decorator está diciendo que el usuario debe estar registrado en la página para activar el view de abajo, de lo contrario, se activara la instrucción del decorator el cual va a mandar al usuario a la página de login.
def RestoreUser_detail(request, id):
	restoreUser_request_instance = RestoreUser_Request.objects.get(id=id)
	userInstance = User.objects.get(id = restoreUser_request_instance.id_user.id)

	context = {
		'RestoreRequest':restoreUser_request_instance,
		'user':userInstance,
	}

	return render(request, "Accounts/RestoreUser_detail.html", context)