
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Libro(models.Model):
    _name = "unicah.biblioteca.libro"
    _description = "Libro de biblioteca UNICAH"
    _order = "name"

    name = fields.Char(
        string="Nombre del libro",
        required=True
    )

    isbn = fields.Char(
        string="ISBN",
        required=True
    )

    autor = fields.Char(
        string="Autor",
        required=True
    )

    categoria_id = fields.Many2one(
        "unicah.biblioteca.categoria",
        string="Categoría",
        required=True,
        ondelete="restrict"
    )

    precio = fields.Float(
        string="Precio",
        required=True,
        default=0.0
    )

    existencias = fields.Integer(
        string="Existencias",
        default=0
    )

    valor_inventario = fields.Float(
        string="Valor del inventario",
        compute="_compute_valor_inventario",
        store=True
    )

    @api.depends("precio", "existencias")
    def _compute_valor_inventario(self):
        for libro in self:
            libro.valor_inventario = libro.precio * libro.existencias

    @api.constrains("precio", "existencias")
    def _check_valores(self):
        for libro in self:
            if libro.precio < 0:
                raise ValidationError(
                    _("El precio del libro no puede ser negativo.")
                )

            if libro.existencias < 0:
                raise ValidationError(
                    _("Las existencias no pueden ser negativas.")
                )

    @api.constrains("isbn")
    def _check_isbn(self):
        for libro in self:
            isbn_limpio = libro.isbn.replace("-", "").replace(" ", "")

            if len(isbn_limpio) not in (10, 13):
                raise ValidationError(
                    _("El ISBN debe contener 10 o 13 caracteres numéricos.")
                )

            if not isbn_limpio.isdigit():
                raise ValidationError(
                    _("El ISBN solo puede contener números, espacios o guiones.")
                )



class ProductTemplate(models.Model):
    _inherit = "product.template"

    es_libro_unicah = fields.Boolean(
        string="Libro de biblioteca UNICAH",
        default=False
    )

    isbn_biblioteca = fields.Char(
        string="ISBN de biblioteca"
    )
