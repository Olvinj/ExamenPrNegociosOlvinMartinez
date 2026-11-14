
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from .res_partner import TIPOS_CLIENTE


class TiendaConvenio(models.Model):
    _name = "tienda.convenio"
    _description = "Convenio de descuento"

    name = fields.Char(string="Nombre", required=True)

    tipo_cliente = fields.Selection(
        TIPOS_CLIENTE,
        string="Tipo de cliente",
        required=True,
    )

    porcentaje = fields.Float(
        string="Descuento (%)",
        required=True,
    )

    fecha_inicio = fields.Date(
        string="Desde",
        required=True,
        default=fields.Date.context_today,
    )

    fecha_fin = fields.Date(string="Hasta")

    active = fields.Boolean(string="Activo", default=True)

    @api.constrains("porcentaje")
    def _check_porcentaje(self):
        for convenio in self:
            if not 0 < convenio.porcentaje <= 40:
                raise ValidationError(_(
                    "El descuento debe ser mayor que 0 y no puede superar el 40%."
                ))

    @api.constrains("fecha_inicio", "fecha_fin")
    def _check_fechas(self):
        for convenio in self:
            if (
                convenio.fecha_inicio
                and convenio.fecha_fin
                and convenio.fecha_fin < convenio.fecha_inicio
            ):
                raise ValidationError(_(
                    "La fecha final no puede ser anterior a la fecha inicial."
                ))
