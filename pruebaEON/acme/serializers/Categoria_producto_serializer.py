'''
Especificación del serializador de la entidad Categoria producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from rest_framework import serializers

from acme.models import Categoria_producto

class CategoriaProductoDetailSerializer(serializers.ModelSerializer):
    '''
    Serializa los elementos que se van a mostrar
    de categoria producto.
    '''
    class Meta:
        model = Categoria_producto
        fields = '__all__'
