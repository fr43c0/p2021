from django.conf import settings
from django.conf.urls.static import static
from ponto.views import index,filtros
from django.urls import path
#from users import urls  as users_urls

app_name='ponto'


urlpatterns = [

    
    # path('status/',status,name='status' ),
    path('filtros/', filtros, name='filtros'),
]