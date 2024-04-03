from django.contrib import admin
from .models import Marketplace, DeactivationMarketplace_Request, RestoreMarketplace_Request, ModifyMarketplace_Request

# Register your models here.
admin.site.register(Marketplace)
admin.site.register(ModifyMarketplace_Request)
admin.site.register(DeactivationMarketplace_Request)
admin.site.register(RestoreMarketplace_Request)