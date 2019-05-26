from django.shortcuts import render
from rest_framework import generics
from .models import Dados
from .serializers import DadosSerializer


class ListDadosView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Dados.objects.all()
    serializer_class = DadosSerializer
