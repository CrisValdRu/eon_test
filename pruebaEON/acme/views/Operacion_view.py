'''
Especificación de la vista de Categoria operacion.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 11 de septiombre de 2021
'''
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from acme.serializers import OperacionDetailSerializer
from acme.serializers import OperacionCreateSerializer
from acme.models import Usuario
from acme.models import Producto
from acme.models import Operacion

from ..utils.GenericsView import GetAllGeneric
from ..utils.GenericsView import GetOneGeneric
from ..utils.GenericsView import PostGeneric
from ..utils.GenericsView import PutGeneric

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una '
        +'lista de Operaciones.',
        responses={
            200:OperacionDetailSerializer(many=True),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones POST para crear una operacion.'
        +' !!Nota: para el campo tipo 1 significa COMPRA, 2 VENTA.',
        request_body=OperacionDetailSerializer,
        responses={
            201:OperacionDetailSerializer(many=False),
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
class Operacion_all_view(APIView, GetAllGeneric, PostGeneric):
    '''
    Atiende las peticiones GET para obtener
    una lista de operaciones y peticiones POST
    para registrar nuevas operaciones.
    '''
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OperacionCreateSerializer
        return OperacionDetailSerializer
    def get_queryset(self):
        qs = Operacion.objects.all()
        return qs

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una instancia de '
        +'una operacion.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria de la operacion.',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:OperacionDetailSerializer(many=False),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones PUT para obtener modificar '
        +'la instancia de una operacion.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria de la operacion.',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=OperacionDetailSerializer,
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
        +'la instancia de una operacion.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria de la operacion.',
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
class Operacion_detail_view(APIView, GetOneGeneric, PutGeneric):
    '''
    Atiende las peticiones GET, PUT, DELETE para 
    obtener, actualizar o eliminar una instancia de una operacion.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OperacionDetailSerializer
        return OperacionDetailSerializer
    def get_object(self):
        try:
            operacion = Operacion.objects.get(id=self.kwargs['id'])
        except Operacion.DoesNotExist:
            operacion = None
        return operacion
    def conditions(self):
        '''
        Condiciones para eliminar una operacion de la base de datos.
        '''
        respuesta: bool
        objeto = self.get_object()
        operaciones = Operacion.objects.filter(usuario__id=objeto.id)
        if len(operaciones) <= 0:
            respuesta = True
        else:
            respuesta = False
        return respuesta
    def delete(self, request, *args, **kwargs):
        '''
        Método que se encarga de eliminar un elemento. 
        '''
        response: Response = Response()
        objeto = self.get_object()
        if objeto is not None:
            if True: # cabiar para hacer el roll back du usuarios y productos
                objeto.delete()
                response.status_code = status.HTTP_200_OK
            else:
                response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        else:
            response.status_code = status.HTTP_204_NO_CONTENT 
        return response
