
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class CategoriaLibro(models.Model):
    _name = "unicah.biblioteca.categoria"
    _description = "Categoría de libros"
    _order = "name"

    name = fields.Char(
        string="Nombre de la categoría",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    active = fields.Boolean(
        string="Activo",
        default=True
    )

    libro_ids = fields.One2many(
        "unicah.biblioteca.libro",
        "categoria_id",
        string="Libros"
    )

    cantidad_libros = fields.Integer(
        string="Cantidad de libros",
        compute="_compute_cantidad_libros"
    )

    def _compute_cantidad_libros(self):
        for categoria in self:
            categoria.cantidad_libros = len(categoria.libro_ids)

