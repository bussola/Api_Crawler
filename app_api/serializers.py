from rest_framework import serializers
from .models import Dados


class DadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dados
        fields = ("categoria","title", "body")