from odoo import fields, models, api


class BookingDeliveryBoysWizard(models.TransientModel):
    _name = 'booking.delivery.boys.wizard'
    _description = 'This module fills and confirms info about shipment creating handover to internal carriers.'

    def _get_delivery_order(self):
        return self.env['stock.picking'].sudo().search([('id', '=', self._context.get('default_deli_order_id'))], limit=1)

    def _get_info_receiver(self):
        return self.env['res.partner'].sudo().search([('id', '=', self._get_delivery_order().partner_id.id)], limit=1)

    name = fields.Char(string='Name', readonly=True)
    delivery_boy_id = fields.Many2one('res.partner', 'Delivery Boy', required=True)
    delivery_boy_phone = fields.Char(related='delivery_boy_id.phone', string='Phone', required=True, readonly=True)
    receiver_id = fields.Many2one('res.partner', 'Receiver', default=_get_info_receiver, required=True, readonly=True, tracking=True)
    street = fields.Char(related='receiver_id.street', string='Street', readonly=True)
    street2 = fields.Char(related='receiver_id.street2', string='Street 2', readonly=True)
    ward_id = fields.Many2one('res.ward', related='receiver_id.ward_id', string='Ward', readonly=True)
    district_id = fields.Many2one('res.district', related='receiver_id.district_id', string='District', readonly=True)
    city_id = fields.Many2one('res.city', related='receiver_id.city_id', string='City', readonly=True)
    receiver_phone = fields.Char(related='receiver_id.phone', string='Phone', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    delivery_order_id = fields.Many2one('stock.picking', string='Delivery order', default=_get_delivery_order, required=True, readonly=True)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id')
    cod = fields.Monetary(string='COD', currency_field='currency_id')

    def action_booking_delivery_boys(self):
        pass