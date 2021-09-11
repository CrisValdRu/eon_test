'''
Especificación de la vista de Categoria producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 11 de septiombre de 2021
'''
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView

from acme.serializers import ProductoDetailSerializer
from acme.models import Producto
from acme.models import Operacion

from ..utils.GenericsView import GetAllGeneric
from ..utils.GenericsView import GetOneGeneric
from ..utils.GenericsView import PostGeneric
from ..utils.GenericsView import PutGeneric
from ..utils.GenericsView import DeleteGeneric

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una '
        +'lista de productos.',
        responses={
            200:ProductoDetailSerializer(many=True),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones POST para crear un producto.',
        request_body=ProductoDetailSerializer,
        responses={
            201:ProductoDetailSerializer(many=False),
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
class Producto_all_view(APIView, GetAllGeneric, PostGeneric):
    '''
    Atiende las peticiones GET para obtener
    una lista de productos y peticiones POST
    para registrar nuevos productos.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductoDetailSerializer
        return ProductoDetailSerializer
    def get_queryset(self):
        qs = Producto.objects.all()
        return qs

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una instancia de '
        +'un producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del producto.',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:ProductoDetailSerializer(many=False),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones PUT para obtener modificar '
        +'la instancia de un producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del producto.',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=ProductoDetailSerializer,
        responses={
            200:'Operación exitosa',
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones DELETE para eliminar '
        +'la instancia de un producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria de la producto.',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:'Operación exitosa',
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
class Producto_detail_view(APIView, GetOneGeneric, PutGeneric, DeleteGeneric):
    '''
    Atiende las peticiones GET, PUT, DELETE para 
    obtener, actualizar o eliminar una instancia de producto.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductoDetailSerializer
        return ProductoDetailSerializer
    def get_object(self):
        try:
            producto = Producto.objects.get(id=self.kwargs['id'])
        except Producto.DoesNotExist:
            producto = None
        return producto
    def conditions(self):
        '''
        Condiciones para eliminar una categoria de la base de datos.
        '''
        respuesta: bool
        objeto = self.get_object()
        operaciones = Operacion.objects.filter(producto__id=objeto.id)
        if len(operaciones) <= 0:
            respuesta = True
        else:
            respuesta = False
        return respuesta
