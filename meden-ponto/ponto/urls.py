from django.conf import settings
from django.conf.urls.static import static
from ponto.views import filtros,derrubar
from django.urls import path
#from users import urls  as users_urls
app_name='ponto'


urlpatterns = [
    path('filtros/', filtros, name='filtros'),
    path('derrubar/@3npk!**()z54A/', derrubar, name='derrubar'),
]
