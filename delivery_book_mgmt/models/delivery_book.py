from odoo import models, fields


class DeliveryBook(models.Model):
    _name = 'delivery.book'
    _inherit = ['mail.thread']
    _rec_name = 'bl_code'
    _description = 'Manage deliveries by home shipper'

    carrier_id = fields.Many2one('delivery.carrier', string='Shipping method', required=True, tracking=True)
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, tracking=True)
    sale_id = fields.Many2one(related='deli_order_id.sale_id', string='Sale order')
    fee_ship = fields.Monetary(string='Fee ship', required=True, tracking=True)
    bl_code = fields.Char(string='B/L Code', required=True, readonly=True)
    num_of_package = fields.Integer(string='Number of package', tracking=True)
    partner_id = fields.Many2one(related='deli_order_id.partner_id', string='Customer', required=True, tracking=True)
    street = fields.Char(related='partner_id.street', string='Street')
    street2 = fields.Char(related='partner_id.street2', string='Street 2')
    ward_id = fields.Many2one(related='partner_id.ward_id', string='Ward')
    district_id = fields.Many2one(related='partner_id.district_id', string='District')
    city_id = fields.Many2one(related='partner_id.city_id', string='City')
    partner_phone = fields.Char(related='partner_id.phone', string='Phone')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    cod = fields.Monetary(string='COD', currency_field='currency_id', tracking=True)
    state = fields.Char(string='State', required=True, tracking=True, readonly=True)
    est_deli_time = fields.Float(string='Est Delivery Time')
    note = fields.Text(string='Note')
