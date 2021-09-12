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
    def create(self, validated_data):
        try:
            with transaction.atomic():
                produto = Producto(**validated_data)
                if produto.precio <= 0.50:
                    raise serializers.ValidationError('El precio minimo es 0.50')
                if produto.existencia < 1:
                    raise serializers.ValidationError('La existencia minima es 1')
                produto.save()
        except ValidationError as exce:
            raise serializers.ValidationError(exce.detail)
        return produto
