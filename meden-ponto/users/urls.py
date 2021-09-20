from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from ponto.views import index
from users import urls  as users_urls

app_name='users'


urlpatterns = [

    
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),{'next_page': '/login'}, name='logout'),
    path('profile/',user_views.UserListView.as_view(template_name='users/perfil.html'),name='perfil'),
    path('geral/',user_views.GeralListView.as_view(template_name='users/geral.html'),name='geral'),#
    path('ranking/',user_views.RankingTemplateView.as_view(template_name='users/ranking.html'),name='ranking'),
    path('permitidos/',user_views.EmailListView.as_view(),name='permitidos'),
    path('permitidos/<int:pk>/',user_views.EmailDetailView.as_view(),name='detalhe'),
    path('deletar/<int:pk>/',user_views.EmailDeleteView.as_view(),name='deletar'),
    path('novo/',user_views.EmailCreateView.as_view(),name='novo'),
    path('participantes/',user_views.ParticipantesTemplateView.as_view(),name='participantes'),
    path('deletar/<int:pk>/del_user',user_views.del_user,name='users/del_user.html'),
]

  
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),{'next_page': '/login'}, name='logout'),
    # path('profile/',user_views.UserListView.as_view(template_name='users/perfil.html'),name='perfil'),
    # path('permitidos/',user_views.EmailListView.as_view(),name='permitidos'),
    # path('permitidos/<int:pk>/',user_views.EmailDetailView.as_view(),name='detalhe'),
    # path('deletar/<int:pk>/',user_views.EmailDeleteView.as_view(),name='deletar'),
    # path('novo/',user_views.EmailCreateView.as_view(),name='novo'),
    # path('participantes/',user_views.ParticipantesTemplateView.as_view(),name='participantes'),
