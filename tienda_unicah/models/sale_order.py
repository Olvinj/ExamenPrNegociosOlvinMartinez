
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tipo_cliente = fields.Selection(
        related="partner_id.tipo_cliente",
        string="Tipo de cliente",
        readonly=True,
    )

    convenio_id = fields.Many2one(
        "tienda.convenio",
        string="Convenio aplicable",
        compute="_compute_convenio",
    )

    monto_ahorro = fields.Monetary(
        string="Monto de ahorro",
        compute="_compute_monto_ahorro",
        currency_field="currency_id",
        store=True,
    )

    @api.depends("partner_id", "date_order", "partner_id.tipo_cliente")
    def _compute_convenio(self):
        for order in self:
            order.convenio_id = False

            if not order.partner_id or not order.partner_id.tipo_cliente:
                continue

            fecha = (
                fields.Date.to_date(order.date_order)
                if order.date_order
                else fields.Date.context_today(order)
            )

            convenio = self.env["tienda.convenio"].search([
                ("tipo_cliente", "=", order.partner_id.tipo_cliente),
                ("active", "=", True),
                ("fecha_inicio", "<=", fecha),
                "|",
                ("fecha_fin", "=", False),
                ("fecha_fin", ">=", fecha),
            ], limit=1, order="porcentaje desc")

            order.convenio_id = convenio

    @api.depends(
        "order_line.price_subtotal",
        "order_line.discount",
        "order_line.price_unit",
        "order_line.product_uom_qty",
    )
    def _compute_monto_ahorro(self):
        for order in self:
            ahorro = 0.0

            for linea in order.order_line.filtered(
                lambda line: not line.display_type
            ):
                ahorro += (
                    linea.price_unit
                    * linea.product_uom_qty
                    * linea.discount
                    / 100
                )

            order.monto_ahorro = ahorro

    def action_aplicar_convenio(self):
        for order in self:
            if not order.convenio_id:
                raise UserError(_("El cliente no tiene un convenio vigente."))

            lineas = order.order_line.filtered(
                lambda line: not line.display_type
            )

            if not lineas:
                raise UserError(_("Agregue al menos un producto al pedido."))

            for linea in lineas:
                linea.discount = order.convenio_id.porcentaje

            order.message_post(
                body=_(
                    "Se aplicó el convenio %s con un descuento del %s%%."
                ) % (
                    order.convenio_id.name,
                    order.convenio_id.porcentaje,
                )
            )

        return True

    def action_confirm(self):
        for order in self:
            tipo = order.partner_id.tipo_cliente

            total_unidades = sum(
                order.order_line.filtered(
                    lambda line: not line.display_type
                ).mapped("product_uom_qty")
            )

            if tipo == "estudiante" and total_unidades > 10:
                raise UserError(_(
                    "Un estudiante no puede confirmar pedidos "
                    "con más de 10 unidades."
                ))

            if tipo == "docente" and total_unidades > 12:
                raise UserError(_(
                    "Un docente no puede confirmar pedidos "
                    "con más de 12 unidades."
                ))

        return super().action_confirm()
