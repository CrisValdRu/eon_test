'''
Vistas genéricas para las diferentes vistas del sistema.

Autor: Cesar Cristian Valdez Ruiz
Fecha de última modificación: 10 de septiembre 2021
'''
from django.core.validators import ValidationError
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

class GetAllGeneric:
    '''
    Clase genérica que se encarga de 
    obtener y serializar una lista de elementos de
    un query set.
    '''
    def get(self, request, *args, **kwargs):
        '''
        Método que se encarga de obtener 
        todas las instancias de un query set.
        '''
        response: Response = Response()
        qs = self.get_queryset()
        if qs.count() == 0:
            response.status_code = status.HTTP_204_NO_CONTENT
        else:
            response.data = self.get_serializer_class()(
                qs,
                many=True,
                context={'request': request}
            ).data
            response.status_code = status.HTTP_200_OK

        return response

class GetOneGeneric:
    '''
    Clase genérica que se encarga de 
    obtener y serializar un elemento de 
    un queryset.
    '''
    def get(self, request, *args, **kwargs):
        '''
        Método que se encarga de obtener 
        una instancia de un query set.
        '''
        response: Response = Response()
        objeto = self.get_object()
        if objeto is not None:
            response.data = self.get_serializer_class()(
                objeto,
                many=False,
                context={'request': request}
            ).data
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
        return response

class PostGeneric:
    '''
    Clase genérica que se encarga de 
    crear un elemento de 
    un modelo.
    '''
    def post(self, request, *args, **kwargs):
        '''
        Método que se encarga de crear 
        una instancia de un modelo.
        '''
        response: Response = Response()
        with transaction.atomic():
            serializador = self.get_serializer_class()(data=request.data)
            try:
                if serializador.is_valid(raise_exception=False):
                    objeto = serializador.create(serializador.validated_data)
                    serializador = self.get_serializer_class()(objeto)
                    response.data = serializador.data
                    response.status_code = status.HTTP_201_CREATED
                else:
                    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                    response.data = serializador.errors
            except ValidationError:
                response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return response

class PutGeneric:
    '''
    Clase genérica que se encarga de 
    actualizar un elemento de 
    un modelo.
    '''
    def put(self, request, *args, **kwargs):
        '''
        Método que se encarga de actualizar 
        una isntancia de un modelo.
        '''
        response: Response = Response()
        objeto = self.get_object()
        if objeto is not None:
            with transaction.atomic():
                serializador = self.get_serializer_class()(objeto, data=request.data)
                try:
                    if serializador.is_valid(raise_exception=False):
                        objeto = serializador.save()
                        serializador = self.get_serializer_class()(objeto)
                        response.data = serializador.data
                        response.status_code = status.HTTP_200_OK
                    else:
                        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                        response.data = serializador.errors
                except ValidationError:
                    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
        return response

class DeleteGeneric:
    '''
    Clase genérica que se encarga de 
    eliminar un elemento de 
    un modelo.
    '''
    def conditions(self):
        '''
        Método que se debe de sobreescribir en caso de que se requiera 
        añadir condiciones para el borrado del elemento.
        '''
        return True
    def delete(self, request, *args, **kwargs):
        '''
        Método que se encarga de eliminar un elemento. 
        '''
        response: Response = Response()
        objeto = self.get_object()
        if objeto is not None:
            if self.conditions():
                objeto.delete()
                response.status_code = status.HTTP_200_OK
            else:
                response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        else:
            response.status_code = status.HTTP_204_NO_CONTENT 
        return response
