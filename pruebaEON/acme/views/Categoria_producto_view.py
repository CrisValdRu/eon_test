'''
Especificación de la vista de Categoria producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 11 de septiombre de 2021
'''
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView

from acme.serializers import CategoriaProductoDetailSerializer
from acme.models import Categoria_producto
from acme.models import Producto

from ..utils.GenericsView import GetAllGeneric
from ..utils.GenericsView import GetOneGeneric
from ..utils.GenericsView import PostGeneric
from ..utils.GenericsView import PutGeneric
from ..utils.GenericsView import DeleteGeneric

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una '
        +'lista de categoria de productos.',
        responses={
            200:CategoriaProductoDetailSerializer(many=True),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones POST para crear una categoria de producto.',
        request_body=CategoriaProductoDetailSerializer,
        responses={
            201:CategoriaProductoDetailSerializer(many=False),
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
class Categoria_producto_all_view(APIView, GetAllGeneric, PostGeneric):
    '''
    Atiende las peticiones GET para obtener
    una lista de categoria de productos y peticiones POST
    para registrar nuevas categorias de productos.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoriaProductoDetailSerializer
        return CategoriaProductoDetailSerializer
    def get_queryset(self):
        qs = Categoria_producto.objects.all()
        return qs

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una instancia de '
        +'un categoria de producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del categoria.',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:CategoriaProductoDetailSerializer(many=False),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones PUT para obtener modificar '
        +'la instancia de una cataloga de producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del categoria.',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=CategoriaProductoDetailSerializer,
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
        +'la instancia de una categoria de producto.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria de la categoria.',
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
class Categoria_producto_detail_view(APIView, GetOneGeneric, PutGeneric, DeleteGeneric):
    '''
    Atiende las peticiones GET, PUT, DELETE para 
    obtener, actualizar o eliminar una instancia de categoria de producto.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoriaProductoDetailSerializer
        return CategoriaProductoDetailSerializer
    def get_object(self):
        try:
            categoria = Categoria_producto.objects.get(id=self.kwargs['id'])
        except Categoria_producto.DoesNotExist:
            categoria = None
        return categoria
    def conditions(self):
        '''
        Condiciones para eliminar una categoria de la base de datos.
        '''
        respuesta: bool
        objeto = self.get_object()
        productos = Producto.objects.filter(categoria__id=objeto.id)
        if len(productos) <= 0:
            respuesta = True
        else:
            respuesta = False
        return respuesta
