'''
Módulo que contiene la uris del subsistema
de acme
'''

from django.urls import path, include

from acme.views import Categoria_producto_all_view
from acme.views import Categoria_producto_detail_view
from acme.views import Producto_all_view
from acme.views import Producto_detail_view
from acme.views import Usuario_all_view
from acme.views import Usuario_detail_view
from acme.views import Operacion_all_view
from acme.views import Operacion_detail_view

CATEGORIAS_URLS = [
    path(
        '',
        Categoria_producto_all_view.as_view(),
        name='categorias-producto-list'
    ),
    path(
        '/categoria-producto/<int:id>',
        Categoria_producto_detail_view.as_view(),
        name='categoria-producto-detail'
    )
]

PRODUCTOS_URLS = [
    path(
        '',
        Producto_all_view.as_view(),
        name='productos-list'
    ),
    path(
        '/producto/<int:id>',
        Producto_detail_view.as_view(),
        name='producto-detail'
    )
]

USUARIOS_URLS = [
    path(
        '',
        Usuario_all_view.as_view(),
        name='usuarios-list'
    ),
    path(
        '/usuario/<int:id>',
        Usuario_detail_view.as_view(),
        name='usuario-detail'
    )
]

OPERACIONES_URLS = [
    path(
        '',
        Operacion_all_view.as_view(),
        name='operaciones-list'
    ),
    path(
        '/operacion/<int:id>',
        Operacion_detail_view.as_view(),
        name='operacion-detail'
    )
]

ACME_URLS = [ 
    path(
        'categorias',
        include(CATEGORIAS_URLS)
    ),
    path(
        'productos',
        include(PRODUCTOS_URLS)
    ),
    path(
        'usuarios',
        include(USUARIOS_URLS)
    ),
    path(
        'operaciones',
        include(OPERACIONES_URLS)
    )
]
