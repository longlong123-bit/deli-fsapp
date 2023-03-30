from odoo import fields, models, api


class BookingDeliveryBoysWizard(models.TransientModel):
    _name = 'booking.delivery.boys.wizard'
    _description = 'This module fills and confirms info about shipment creating handover to internal carriers.'

    name = fields.Char(string='Name', readonly=True)
    delivery_boy_id = fields.Many2one('res.partner', 'Delivery Boy', required=True)
    delivery_boy_phone = fields.Char(related='delivery_boy_id.phone', string='Phone', required=True, readonly=True)
    customer_id = fields.Many2one('res.partner', 'Delivery Boy', required=True, tracking=True)
    street = fields.Char(related='customer_id.street', string='Street', readonly=True)
    street2 = fields.Char(related='customer_id.street2', string='Street 2', readonly=True)
    ward_id = fields.Many2one('res.ward', related='customer_id.ward_id', string='Ward', readonly=True)
    district_id = fields.Many2one('res.district', related='customer_id.district_id', string='District', readonly=True)
    city_id = fields.Many2one('res.city', related='customer_id.city_id', string='City', readonly=True)
    customer_phone = fields.Char(related='customer_id.phone', string='Phone', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    delivery_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id', readonly=True)
    cod = fields.Monetary(string='COD', currency_field='currency_id', readonly=True)

    def action_booking_delivery_boys(self):
        pass