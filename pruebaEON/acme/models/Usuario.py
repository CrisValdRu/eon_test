'''
Especificación de la entidad Usuario.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from django.db import models

class Usuario(models.Model):
    '''
        Almacena la informacion de usuario.
    '''
    nombre = models.CharField(
        max_length=50
    )
    apPaterno = models.CharField(
        max_length=50
    )
    apMaterno = models.CharField(
        max_length=50,
        null=True
    )
    username = models.CharField(
        'username',
        max_length=30
    )
    password = models.CharField(
        'password',
        max_length=50
    )
    saldo = models.FloatField()

    class Meta:
        db_table = 'ACME_Usuario'

    def __str__(self):
        return str(self.nombre)
