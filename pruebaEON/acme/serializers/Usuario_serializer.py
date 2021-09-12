'''
Especificación del serializador de la entidad Usuario.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from rest_framework import serializers

from rest_framework.validators import ValidationError

from django.db import transaction

from acme.models import Usuario

class UsuarioDetailSerializer(serializers.ModelSerializer):
    '''
    Serializa los elementos que se van a mostrar
    de producto.
    '''
    class Meta:
        model = Usuario
        fields = '__all__'
    def create(self, validated_data):
        try:
            with transaction.atomic():
                usuario = Usuario(**validated_data)
                if usuario.saldo < 1000.0:
                    raise serializers.ValidationError('SALDO INSUFICIENTE')
                usuario.save()
        except ValidationError as exce:
            raise serializers.ValidationError(exce.detail)
        return usuario

