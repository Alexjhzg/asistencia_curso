from django.urls import path
from . import views

urlpatterns = [
    path('api/personas/<str:cedula>/', views.PerfilPorCedulaView.as_view(), name='perfil-por-cedula'),
]