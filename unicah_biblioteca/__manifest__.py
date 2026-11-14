
{
    "name": "UNICAH Biblioteca",
    "version": "1.0",
    "summary": "Gestión de libros de la biblioteca universitaria",
    "description": """
        Módulo para administrar libros, categorías,
        autores, precios y existencias de la biblioteca UNICAH.
    """,
    "category": "Services",
    "author": "UNICAH",
    "license": "LGPL-3",
    "depends": [
        "base",
        "product",
    ],
    "data": [
        "security/ir.access.csv",
        "views/categoria_views.xml",
        "views/libro_views.xml",
    ],
    "installable": True,
    "application": True,
}
