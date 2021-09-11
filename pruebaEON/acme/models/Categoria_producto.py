'''
Especificación de la entidad categoria producto.

Autor: Cesar Cristian Valdez Ruiz.
Ultima modificación: 10 de septiembre de 2021
'''
from django.db import models

class Categoria_producto(models.Model):
    '''
        Almacena las categorias de los productos.
    '''
    nombre = models.CharField(
        max_length=50
    )

    class Meta:
        db_table = 'ACME_categoria_producto'

    def __str__(self):
        return str(self.nombre)
