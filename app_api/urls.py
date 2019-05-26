from django.urls import path
from .views import ListDadosView


urlpatterns = [
    path('dados/', ListDadosView.as_view(), name="dados-all")
]