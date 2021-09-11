'''
Especificación de la entidad Producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from django.db import models
from .Categoria_producto import Categoria_producto

class Producto(models.Model):
    '''
        Almacena la informacion de producto.
    '''
    nombre = models.CharField(
        max_length=50
    )
    descripcion = models.CharField(
        max_length=300
    )
    precio = models.FloatField()
    existencia = models.IntegerField()
    categoria = models.ForeignKey(
        'Categoria_producto',
        on_delete=models.PROTECT,
        db_column='CAT_Categoria_id'
    )

    class Meta:
        db_table = 'ACME_Producto'

    def __str__(self):
        return str(self.nombre)
