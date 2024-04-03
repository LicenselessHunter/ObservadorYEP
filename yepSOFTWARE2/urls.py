from django.contrib import admin
from django.urls import path, include
from . import views #Referencio al archivo views para usar sus funciones.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #"staticfiles_urlpatterns" nos va a dejar que se anexe a la urlpatterns y django pueda operar con el funcionamiento de staticfiles.

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.viewHome, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"), 


    path('tables/', include('tables.urls')), #Se incluye el archivo "tables.urls" y con ello acceso a sus url. en la pagina.
    path('Accounts/', include('Accounts.urls')), #Se incluye el archivo "Accounts.urls" y con ello acceso a sus url. en la pagina.
    path('marketplaces/', include('marketplaces.urls')),
    path('Sales/', include('Sales.urls')),
]

urlpatterns += staticfiles_urlpatterns() #A urlpatterns se le está agregando el método "staticfiles_urlpatterns()". Apartir de aquí se le esta diciendo a django como queremos manejar nuestros static files.

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#"+=" Esto se está anexando a urlpatterns. Parametro: "setting.MEDIA_URL" es donde quieres encontrar el media en el navegador. "document_root=settings.MEDIA_ROOT" Es el documento donde estara guardado el media. 
#Ahora que django sabe donde están, va a levantar un "url pattern" para nosotros, para entregarnos estas "medias" cuando las escribamos en el browser o cuando las solicitemos para un template.