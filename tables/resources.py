from import_export import resources, fields
from . import models #Desde "."(directorio actual) se va a importar "models.py"
from import_export.widgets import ForeignKeyWidget
from django.db.models import F
from datetime import datetime
from django.contrib.auth.models import User

class ProductsAdminImportExport(resources.ModelResource):

	created_by = fields.Field(
		column_name='created_by',
		attribute='created_by',
		widget=ForeignKeyWidget(User, 'username'))

	validation_by = fields.Field(
		column_name='validation_by',
		attribute='validation_by',
		widget=ForeignKeyWidget(User, 'username'))


	class Meta:
		model = models.Product