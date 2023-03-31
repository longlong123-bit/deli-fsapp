from odoo import models, fields


class DeliveryBoys(models.Model):
    _name = 'delivery.boys'
    _inherit = ['mail.thread']
    _description = 'Manage deliveries by home shipper'

    name = fields.Char(string='Name', readonly=True)
    deli_boy_id = fields.Many2one('res.partner', 'Delivery Boy', required=True, tracking=True)
    deli_phone = fields.Char(related='partner_id.phone', string='Phone')
    deli_order_id = fields.Many2one('stock.picking', 'Delivery Order', required=True, tracking=True)
    sale_id = fields.Many2one('sale.order', related='deli_order_id.sale_id', string='Sale order')
    partner_id = fields.Many2one('res.partner', 'Receiver', required=True, tracking=True)
    street = fields.Char(related='partner_id.street', string='Street')
    street2 = fields.Char(related='partner_id.street2', string='Street 2')
    ward_id = fields.Many2one('res.ward', related='partner_id.ward_id', string='Ward')
    district_id = fields.Many2one('res.district', related='partner_id.district_id', string='District')
    city_id = fields.Many2one('res.city', related='partner_id.city_id', string='City')
    partner_phone = fields.Char(related='partner_id.phone', string='Phone')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id', tracking=True)
    cod = fields.Monetary(string='COD', currency_field='currency_id', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('inprocess', 'In-process'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    ], default='new')
    num_of_package = fields.Integer(string='Number of package', tracking=True)
    cus_receivable = fields.Monetary(string='Customer\'s Receivable', currency_field='currency_id', tracking=True)
    note = fields.Text(string='Note')

    def action_confirm(self):
        ...

    def action_done(self):
        ...

    def action_refuse(self):
        ...

    def action_cancel(self):
        ...