from odoo import fields, models, api, _


class CancelDeliveryWizard(models.TransientModel):
    _name = 'cancel.delivery.wizard'
    _description = "It's to cancel delivery"

    def _get_delivery_order(self):
        return self.env['stock.picking'].sudo().search([('id', '=', self._context.get('delivery_order_id'))], limit=1)

    delivery_order_id = fields.Many2one('stock.picking', string='Delivery order', default=_get_delivery_order, required=True, readonly=True)
    reason_cancel = fields.Text("Reason", required=True, attachment=True, help="Order confirmation Image")

    def action_confirm_cancel_delivery_boys(self):
        self.delivery_order_id.write({
            'state': 'cancel',
            'note': self.reason_cancel,
        })
