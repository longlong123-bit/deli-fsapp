from odoo import models, fields, api, _


class DeliveryBoys(models.Model):
    _name = 'delivery.boys'
    _inherit = ['mail.thread']
    _description = 'Manage deliveries by home shipper'

    name = fields.Char(string='B/L code', readonly=True)
    deli_boy_id = fields.Many2one('res.partner', 'Delivery Boy', tracking=True)
    deli_phone = fields.Char(string='Phone', tracking=True)
    deli_street = fields.Char(string='Street')
    deli_ward_id = fields.Many2one('res.ward', string='Ward')
    deli_district_id = fields.Many2one('res.district', string='District')
    deli_province_id = fields.Many2one('res.city', string='Province')

    deli_order_id = fields.Many2one('stock.picking', 'Delivery Order', readonly=True, required=True, tracking=True)
    sale_id = fields.Many2one('sale.order', related='deli_order_id.sale_id', string='Sale order')
    partner_id = fields.Many2one('res.partner', 'Receiver', required=True, tracking=True)
    street = fields.Char(related='partner_id.street', string='Street')
    ward_id = fields.Many2one('res.ward', related='partner_id.ward_id', string='Ward')
    district_id = fields.Many2one('res.district', related='partner_id.district_id', string='District')
    city_id = fields.Many2one('res.city', related='partner_id.city_id', string='City')
    partner_phone = fields.Char(string='Phone', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id', tracking=True)
    cod = fields.Monetary(string='COD', currency_field='currency_id', tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_process', 'In process'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    ], default='new')
    num_of_package = fields.Integer(string='Number of package', tracking=True)
    cus_receivable = fields.Monetary(string='Cus\'s Receivable', currency_field='currency_id', tracking=True)
    note = fields.Text(string='Note')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    weight = fields.Float(string='Weight')
    est_deli_time = fields.Integer(string='Estimate delivery')
    cancel_reason = fields.Text(string='Cancel reason')

    def _get_default_hours_uom_name(self):
        return self._get_hours_uom_name()

    def _get_default_gram_uom_name(self):
        return self._get_gram_uom_name()

    hours_uom_name = fields.Char(string='Hours unit of measure label', default=_get_default_hours_uom_name,
                                 compute='_compute_hours_uom_name')

    gram_uom_name = fields.Char(string='Gram unit of measure label', default=_get_default_gram_uom_name,
                                compute='_compute_gram_uom_name')

    @api.model
    def _get_hours_uom_name(self):
        return self.env.ref('uom.product_uom_hour').display_name

    @api.model
    def _get_gram_uom_name(self):
        return self.env.ref('uom.product_uom_gram').display_name

    def _compute_hours_uom_name(self):
        for rec in self:
            rec.hours_uom_name = self._get_hours_uom_name()

    def _compute_gram_uom_name(self):
        for rec in self:
            rec.gram_uom_name = self._get_gram_uom_name()

    @api.onchange('deli_boy_id')
    def _onchange_delivery_boy_phone(self):
        if self.deli_boy_id:
            self.deli_phone = self.deli_boy_id.phone
            self.deli_street = self.deli_boy_id.street
            self.deli_ward_id = self.deli_boy_id.ward_id.id
            self.deli_district_id = self.deli_boy_id.district_id.id
            self.deli_province_id = self.deli_boy_id.city_id.id

    @api.onchange('partner_id')
    def _onchange_partner_phone(self):
        if self.partner_id:
            self.partner_phone = self.partner_id.phone

    def _get_payload_delivery_book(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        action_id = self.env.ref('delivery_boys_mgmt.delivery_boys_action_view').id
        tracking_link = f"{base_url}/web#id={self.id}&action={action_id}&model={self._name}&view_type=form"
        carrier_id = self.env['delivery.carrier'].search([('delivery_type', '=', 'deli_boys')])
        payload = {
            'carrier_id': carrier_id.id,
            'receiver_id': self.partner_id.id,
            'receiver_phone': self.partner_phone,
            'receiver_street': self.street,
            'receiver_ward_id': self.ward_id.id,
            'receiver_district_id': self.district_id.id,
            'receiver_province_id': self.city_id.id,
            'sender_id': self.warehouse_id.id,
            'deli_boy_id': self.deli_boy_id.id,
            'sender_street': self.deli_street,
            'sender_ward_id': self.deli_ward_id.id,
            'sender_district_id': self.deli_district_id.id,
            'sender_province_id': self.deli_province_id.id,
            'sender_phone': self.deli_phone,
            'deli_order_id': self.deli_order_id.id,
            'note': self.note,
            'num_of_package': self.num_of_package,
            'fee_ship': self.fee_ship,
            'bl_code': self.name,
            'cod': self.cod,
            'weight': self.weight,
            'est_deli_time': self.est_deli_time,
            'tracking_link': tracking_link,
            'cus_receivable': self.cus_receivable,
            'state': 'Shipper đã nhận hàng',
        }
        return payload

    def action_confirm(self):
        payload = self._get_payload_delivery_book()
        delivery_book_id = self.env['delivery.book'].sudo().create(payload)
        self.write({'state': 'assigned'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Book',
            'res_model': 'delivery.book',
            'view_mode': 'form',
            'res_id': delivery_book_id.id,
            'target': 'current',
        }

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
        self.write({
            'state': 'new',
            'deli_boy_id': False,
            'deli_phone': False,
            'deli_street': False,
            'deli_ward_id': False,
            'deli_district_id': False,
            'deli_province_id': False
        })

    def action_cancel(self):
        return {
            'name': _('Cancel delivery'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('delivery_boys_mgmt.cancel_delivery_boys_wizard_form_view').id,
            'res_model': 'cancel.delivery.boys.wizard',
            'context': {
                'delivery_order_id': self.deli_order_id.id,
            },
            'type': 'ir.actions.act_window',
            'target': 'new'
        }