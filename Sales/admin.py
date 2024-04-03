from django.contrib import admin
from .models import sale, Sales_group
from import_export.admin import ImportExportModelAdmin
from .resources import SalesAdminImportExport, Group_saleAdminImportExport

class sales_admin_import_export(ImportExportModelAdmin):
     resource_class = SalesAdminImportExport

class GroupSale_admin_import_export(ImportExportModelAdmin):
     resource_class = Group_saleAdminImportExport

# Register your models here.
admin.site.register(sale, sales_admin_import_export)
admin.site.register(Sales_group, GroupSale_admin_import_export)