'''
Especificación del serializador de la entidad Operacion.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from os import read, write
from rest_framework import serializers

from rest_framework.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from datetime import datetime

from acme.models import Producto
from acme.models import Usuario
from acme.models import Operacion

from acme.utils.Constants import TIPO_OPERACION_COMPRA
from acme.utils.Constants import TIPO_OPERACION_VENTA
from acme.utils.Constants import TEXT_OPERACION_COMPRA
from acme.utils.Constants import TEXT_OPERACION_VENTA

class OperacionDetailSerializer(serializers.ModelSerializer):
    '''
    Serializa los elementos que se van a mostrar
    de producto.
    '''
    class Meta:
        model = Operacion
        fields = '__all__'

class OperacionCreateSerializer(serializers.Serializer):
    '''
    Serializa los elementos que se van a mostrar
    de producto.
    '''
    cantidad = serializers.IntegerField(write_only=True)
    tipo = serializers.IntegerField(write_only=True)
    usuario = serializers.IntegerField(write_only=True)
    producto = serializers.IntegerField(write_only=True)
    operacion_datos = serializers.SerializerMethodField(
        method_name='get_operacion',
        read_only=True
    )
    def get_operacion(self, obj:Operacion):
        data = {
            'id': obj.id,
            'fecha': obj.fecha,
            'producto_id': obj.producto.id,
            'producto_existencias': obj.producto.existencia,
            'usuario_nombre': obj.usuario.nombre,
            'usuario_saldo': obj.usuario.saldo,
            'cantidad': obj.cantidad,
            'precio': obj.precio,
            'tipo': TEXT_OPERACION_COMPRA if obj.tipo == TIPO_OPERACION_COMPRA else TEXT_OPERACION_VENTA,
        }
        return data
    def validate_compra(self, operacion: Operacion, producto: Producto, usuario: Usuario):
        is_valid = True
        if operacion.cantidad <= 0:
            is_valid = False
        if not producto.existencia - operacion.cantidad >= 0:
            is_valid = False
        if not usuario.saldo - operacion.precio >=0 :
            is_valid = False
        if not is_valid:
            raise serializers.ValidationError('Sin existencias o saldo suficiente o cantidad menor a cero')
    def validate_venta(self, operacion: Operacion, producto: Producto, usuario: Usuario):
        is_valid = True
        if operacion.cantidad <= 0:
            is_valid = False
        if not is_valid:
            raise serializers.ValidationError('Cantidad menor a cero')
    def createCampra(self, operacion: Operacion):
        producto = Producto.objects.get(id=operacion.producto_id)
        usuario = Usuario.objects.get(id=operacion.usuario_id)
        operacion.precio = operacion.cantidad * producto.precio
        self.validate_compra(operacion, producto, usuario)
        producto.existencia -= operacion.cantidad
        usuario.saldo -= operacion.precio
        operacion.usuario = usuario
        operacion.producto = producto
        producto.save()
        usuario.save()
        return operacion
    def createVenta(self, operacion: Operacion):
        producto = Producto.objects.get(id=operacion.producto_id)
        usuario = Usuario.objects.get(id=operacion.usuario_id)
        operacion.precio = operacion.cantidad * producto.precio
        self.validate_venta(operacion, producto, usuario)
        producto.existencia += operacion.cantidad
        usuario.saldo += operacion.precio
        operacion.usuario = usuario
        operacion.producto = producto
        producto.save()
        usuario.save()
        return operacion
    def create(self, validated_data):
        try:
            with transaction.atomic():
                producto = Producto.objects.get(
                    id=validated_data.pop('producto')
                )
                usuario = Usuario.objects.get(
                    id=validated_data.pop('usuario')
                )
                operacion = Operacion(**validated_data)
                operacion.usuario = usuario
                operacion.producto = producto
                if operacion.tipo is TIPO_OPERACION_COMPRA:
                    operacion = self.createCampra(operacion)
                elif operacion.tipo is TIPO_OPERACION_VENTA:
                    operacion = self.createVenta(operacion)
                else:
                    raise serializers.ValidationError('Tipo no valido')
                operacion.fecha = datetime.now()
                operacion.save()
                
        except ValidationError as exce:
            raise serializers.ValidationError(exce.detail)
        except ObjectDoesNotExist as ode:
            raise serializers.ValidationError(ode)

        return operacion
