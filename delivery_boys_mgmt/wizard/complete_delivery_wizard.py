from odoo import fields, models, api


class CompleteDeliveryWizard(models.TransientModel):
    _name = 'complete.delivery.wizard'
    _description = 'It to confirm order delivery successfully'

    def _get_delivery_order(self):
        return self.env['stock.picking'].sudo().search([('id', '=', self._context.get('delivery_order_id'))], limit=1)

    delivery_order_id = fields.Many2one('stock.picking', string='Delivery order', default=_get_delivery_order, required=True, readonly=True)
    order_confirmation_image = fields.Binary("Order confirmation Image", required=True, attachment=True, help="Order confirmation Image")

    def action_confirm_delivery_boys(self):
        self.env['ir.attachment'].sudo().create({
            'name': '%s - %s - %s' % ("Confirm delivery", self.delivery_order_id.delivery_order_id.name, self.delivery_order_id.name),
            'res_id': self._context.get('delivery_boys_id'),
            'res_model': 'delivery.boys',
            'datas': self.order_confirmation_image,
            'public': True,
        })
        self.delivery_order_id.write({
            'state': 'done'
        })