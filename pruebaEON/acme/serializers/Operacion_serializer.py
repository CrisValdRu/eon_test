'''
Especificación del serializador de la entidad Operacion.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from rest_framework import serializers

from acme.models import Operacion

class OperacionDetailSerializer(serializers.ModelSerializer):
    '''
    Serializa los elementos que se van a mostrar
    de producto.
    '''
    class Meta:
        model = Operacion
        fields = '__all__'
