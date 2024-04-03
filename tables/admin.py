from django.contrib import admin
from .models import Product, DeactivationProduct_Request, RestoreProduct_Request, ModifyProduct_Request
from import_export.admin import ImportExportModelAdmin
from .resources import ProductsAdminImportExport

class products_admin_import_export(ImportExportModelAdmin):
     resource_class = ProductsAdminImportExport

# Register your models here.

admin.site.register(Product, products_admin_import_export) #Instrucción para registrar modelo "Product"
admin.site.register(ModifyProduct_Request)
admin.site.register(DeactivationProduct_Request)
admin.site.register(RestoreProduct_Request)