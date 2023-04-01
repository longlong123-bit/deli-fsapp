from odoo import models, fields, api, _


class DeliveryBoys(models.Model):
    _name = 'delivery.boys'
    _inherit = ['mail.thread']
    _description = 'Manage deliveries by home shipper'

    name = fields.Char(string='Name', readonly=True)
    deli_boy_id = fields.Many2one('res.partner', 'Delivery Boy', tracking=True)
    # deli_phone = fields.Char(related='deli_boy_id.phone', string='Phone')
    deli_phone = fields.Char(string='Phone', tracking=True)
    deli_order_id = fields.Many2one('stock.picking', 'Delivery Order', readonly=True, required=True, tracking=True)
    sale_id = fields.Many2one('sale.order', related='deli_order_id.sale_id', string='Sale order')
    partner_id = fields.Many2one('res.partner', 'Receiver', required=True, tracking=True)
    street = fields.Char(related='partner_id.street', string='Street')
    street2 = fields.Char(related='partner_id.street2', string='Street 2')
    ward_id = fields.Many2one('res.ward', related='partner_id.ward_id', string='Ward')
    district_id = fields.Many2one('res.district', related='partner_id.district_id', string='District')
    city_id = fields.Many2one('res.city', related='partner_id.city_id', string='City')
    # partner_phone = fields.Char(related='partner_id.phone', string='Phone')
    partner_phone = fields.Char(string='Phone', tracking=True)
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

    @api.onchange('deli_boy_id')
    def _onchange_delivery_boy_phone(self):
        if self.deli_boy_id:
            self.deli_phone = self.deli_boy_id.phone

    @api.onchange('partner_id')
    def _onchange_partner_phone(self):
        if self.partner_id:
            self.partner_phone = self.partner_id.phone

    def action_confirm(self):
        self.state = 'assigned'
        self.deli_order_id.write({
            'carrier_id': self.deli_boy_id.id,
            'carrier_tracking_ref': self.name,
        })

    def action_done(self):
        return {
            'name': _('Complete delivery'),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('delivery_boys_mgmt.complete_delivery_wizard_form_view').id,
            'res_model': 'complete.delivery.wizard',
            'context': {
                'delivery_order_id': self.deli_order_id.id,
                'delivery_boys_id': self.id,
            },
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    def action_refuse(self):
        self.state = 'new'
        self.update({
            'deli_boy_id': None,
            'deli_phone': None
        })

    def action_cancel(self):
        return {
            'name': _('Cancel delivery'),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('delivery_boys_mgmt.cancel_delivery_wizard_form_view').id,
            'res_model': 'cancel.delivery.wizard',
            'context': {
                'delivery_order_id': self.deli_order_id.id,
            },
            'type': 'ir.actions.act_window',
            'target': 'new'
        }