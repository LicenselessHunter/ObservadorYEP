from django.contrib import admin
from .models import Profile, DeactivationUser_Request, RestoreUser_Request, Invitation

# Register your models here.

admin.site.register(Profile) #Instrucción para registrar modelo "Profile"
admin.site.register(DeactivationUser_Request)
admin.site.register(RestoreUser_Request)
admin.site.register(Invitation)