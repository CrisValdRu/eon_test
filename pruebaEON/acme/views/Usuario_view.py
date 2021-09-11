'''
Especificación de la vista de Categoria usuario.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 11 de septiombre de 2021
'''
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView

from acme.serializers import UsuarioDetailSerializer
from acme.models import Usuario
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
        +'lista de Usuarios.',
        responses={
            200:UsuarioDetailSerializer(many=True),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones POST para crear un usuario.',
        request_body=UsuarioDetailSerializer,
        responses={
            201:UsuarioDetailSerializer(many=False),
            400:'Ocurrió un error inesperado.',
            406:'Error de validación.'
        }
    )
)
class Usuario_all_view(APIView, GetAllGeneric, PostGeneric):
    '''
    Atiende las peticiones GET para obtener
    una lista de usuarios y peticiones POST
    para registrar nuevos usuarios.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsuarioDetailSerializer
        return UsuarioDetailSerializer
    def get_queryset(self):
        qs = Usuario.objects.all()
        return qs

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones GET para obtener una instancia de '
        +'un usuario.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del usuario.',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:UsuarioDetailSerializer(many=False),
            204:'No se encontró ninguna coincidencia.',
            406:'Error de validación.'
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description='Atiende las peticiones PUT para obtener modificar '
        +'la instancia de un usuario.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del usuario.',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=UsuarioDetailSerializer,
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
        +'la instancia de un usuario.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                'Llave primaria del usuario.',
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
class Usuario_detail_view(APIView, GetOneGeneric, PutGeneric, DeleteGeneric):
    '''
    Atiende las peticiones GET, PUT, DELETE para 
    obtener, actualizar o eliminar una instancia de usuario.
    '''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsuarioDetailSerializer
        return UsuarioDetailSerializer
    def get_object(self):
        try:
            usuario = Usuario.objects.get(id=self.kwargs['id'])
        except Usuario.DoesNotExist:
            usuario = None
        return usuario
    def conditions(self):
        '''
        Condiciones para eliminar un usuario de la base de datos.
        '''
        respuesta: bool
        objeto = self.get_object()
        operaciones = Operacion.objects.filter(usuario__id=objeto.id)
        if len(operaciones) <= 0:
            respuesta = True
        else:
            respuesta = False
        return respuesta
