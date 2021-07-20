from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registro', views.registro),
    path('logearse',views.logearse),
    path('wall',views.wall),
    path('logout',views.logout),
    path('colaborador',views.colaborador),
    path('administrador',views.administrador),
    path('new_post', views.nuevoMensaje),
    path('delete_post',views.borrarMensaje),
    path('new_comment',views.comentarMensaje)

]
