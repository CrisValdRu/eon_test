'''
Especificación de la entidad Operacion.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from django.db import models
from .Usuario import Usuario
from .Producto import Producto

class Operacion(models.Model):
    '''
        Almacena la informacion de Operacion.
    '''
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    precio = models.FloatField()
    tipo = models.IntegerField()
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT,
        db_column='USU_Usuario_id'
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT,
        db_column='PRO_Producto_id'
    )

    class Meta:
        db_table = 'ACME_Operacion'

    def __str__(self):
        return str(self.precio)
