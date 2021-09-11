'''
Especificación del serializador de la entidad Producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from rest_framework import serializers

from acme.models import Producto

class ProductoDetailSerializer(serializers.ModelSerializer):
    '''
    Serializa los elementos que se van a mostrar
    de producto.
    '''
    class Meta:
        model = Producto
        fields = '__all__'
