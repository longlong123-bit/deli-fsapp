from odoo import fields, models, api


class DeliveryBoysWizard(models.TransientModel):
    _name = 'delivery.boys.wizard'

    deli_boy_id = fields.Many2one('res.partner', 'Delivery Boy', required=True, tracking=True)
    deli_phone = fields.Char(related='partner_id.phone', string='Phone', readonly=True)
    deli_order_id = fields.Many2one('stock.picking', 'Delivery Order', required=True, tracking=True, readonly=True)
    customer_id = fields.Many2one('res.partner', 'Delivery Boy', required=True, tracking=True)
    street = fields.Char(related='partner_id.street', string='Street', readonly=True)
    street2 = fields.Char(related='partner_id.street2', string='Street 2', readonly=True)
    ward_id = fields.Many2one('res.ward', related='partner_id.ward_id', string='Ward', readonly=True)
    district_id = fields.Many2one('res.district', related='partner_id.district_id', string='District', readonly=True)
    city_id = fields.Many2one('res.city', related='partner_id.city_id', string='City', readonly=True)
    customer_phone = fields.Char(related='partner_id.phone', string='Phone', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id', required=True, tracking=True)
    cod = fields.Monetary(string='COD', currency_field='currency_id', required=True, tracking=True)
