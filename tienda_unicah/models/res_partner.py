
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


TIPOS_CLIENTE = [
    ("estudiante", "Estudiante"),
    ("docente", "Docente"),
    ("administrativo", "Administrativo"),
    ("externo", "Externo"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    tipo_cliente = fields.Selection(
        TIPOS_CLIENTE,
        string="Tipo de cliente",
        default="externo",
    )

    numero_cuenta = fields.Char(
        string="Número de cuenta",
        copy=False,
    )

    carrera = fields.Char(
        string="Carrera",
    )

    @api.constrains("numero_cuenta", "tipo_cliente")
    def _check_numero_cuenta(self):
        for partner in self:
            if partner.tipo_cliente == "estudiante":
                if not partner.numero_cuenta or not re.fullmatch(
                    r"\d{10}", partner.numero_cuenta
                ):
                    raise ValidationError(_(
                        "El número de cuenta del estudiante "
                        "debe contener exactamente 10 dígitos."
                    ))
