from odoo import models, fields, _
from odoo.addons.stock_extend.wizard.booking_delivery_boys_wizard import BookingDeliveryBoysWizard


class DeliveryBook(models.Model):
    _name = 'delivery.book'
    _inherit = ['mail.thread']
    _rec_name = 'bl_code'
    _description = 'Manage deliveries by home shipper'

    carrier_id = fields.Many2one('delivery.carrier', string='Shipping Method', required=True, tracking=True)
    carrier_type = fields.Selection(related='carrier_id.delivery_type')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    service_type = fields.Selection(
        selection=lambda self: BookingDeliveryBoysWizard.get_viettelpost_service_types(), string='Service Type', default='VCN')
    order_payment = fields.Selection(selection=lambda self: BookingDeliveryBoysWizard.viettelpost_order_payments(),
                                     string='Order Payment', default='1')
    product_type = fields.Selection(selection=lambda self: BookingDeliveryBoysWizard.viettelpost_product_types(),
                                    string='Product Type', default='HH')
    national_type = fields.Selection(selection=lambda self: BookingDeliveryBoysWizard.viettelpost_national_types(),
                                     string='National Type', default='1')

    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True)
    receiver_phone = fields.Char(string='Phone', required=True)
    receiver_street = fields.Char(string='Street', required=True)
    receiver_ward_id = fields.Many2one('res.ward', string='Ward', required=True)
    receiver_district_id = fields.Many2one('res.district', string='District', required=True)
    receiver_province_id = fields.Many2one('res.city', string='Province', required=True)

    sender_id = fields.Many2one('stock.warehouse', string='Sender', required=True)
    sender_phone = fields.Char(string='Phone', required=True)
    sender_street = fields.Char(string='Address')
    sender_ward_id = fields.Many2one('res.ward', string='Ward')
    sender_district_id = fields.Many2one('res.district', string='District')
    sender_province_id = fields.Many2one('res.city', string='Province')
    deli_boy_id = fields.Many2one('res.partner', string='Deli Boy')
    store_id = fields.Many2one('viettelpost.store', string='Store')
    cus_receivable = fields.Monetary(string='Cus\'s Receivable', currency_field='currency_id')
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, tracking=True)
    sale_id = fields.Many2one(related='deli_order_id.sale_id', string='Sale order')
    note = fields.Text(string='Note')
    num_of_package = fields.Integer(string='Number of package', tracking=True)
    fee_ship = fields.Monetary(string='Fee ship', required=True, tracking=True)
    bl_code = fields.Char(string='B/L Code', required=True, readonly=True)
    cod = fields.Monetary(string='COD', currency_field='currency_id', tracking=True)
    weight = fields.Float(string='Weight')
    state = fields.Char(string='State', required=True, tracking=True, readonly=True)
    est_deli_time = fields.Float(string='Est Delivery Time')
    tracking_link = fields.Char(string='Tracking link', required=True)
    money_total = fields.Monetary(string='Money total', readonly=True, currency_field='currency_id')
    money_fee = fields.Monetary(string='Money fee', readonly=True, currency_field='currency_id')
    money_collection_fee = fields.Monetary(string='Money collection fee', readonly=True,
                                           currency_field='currency_id')
    money_vat = fields.Monetary(string='Money VAT', readonly=True, currency_field='currency_id')
    money_other_fee = fields.Monetary(string='Money other fee', readonly=True, currency_field='currency_id')