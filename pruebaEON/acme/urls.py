'''
Módulo que contiene la uris del subsistema
de acme
'''

from django.urls import path, include

from acme.views import Categoria_producto_all_view
from acme.views import Categoria_producto_detail_view

CATEGORIAS_URLS = [
    path(
        '',
        Categoria_producto_all_view.as_view(),
        name='categorias-producto-list'
    ),
    path(
        '/categoria-producto<int:id>',
        Categoria_producto_detail_view.as_view(),
        name='modulo-detail'
    )
]

ACME_URLS = [ 
    path(
        'categorias',
        include(CATEGORIAS_URLS)
    ),
]
