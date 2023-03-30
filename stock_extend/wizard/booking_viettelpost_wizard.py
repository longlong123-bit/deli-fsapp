from odoo import models, fields, api


class BookingViettelpostWizard(models.TransientModel):
    _name = 'booking.viettelpost.wizard'
    _description = 'This module fills and confirms info about shipment before creating a bill of lading Viettelpost.'

    service_type = fields.Selection(
        selection=lambda self: self.env['delivery.carrier']._get_viettelpost_service_types(),
        string='Service Type', default='VCN')
    order_payment = fields.Selection(selection=lambda self: self.env['delivery.carrier']._viettelpost_order_payments(),
                                     string='ViettelPost Order Payment', default='1')
    product_type = fields.Selection(selection=lambda self: self.env['delivery.carrier']._viettelpost_product_types(),
                                    string='ViettelPost Product Type', default='HH')
    national_type = fields.Selection(selection=lambda self: self.env['delivery.carrier']._viettelpost_national_types(),
                                     string='ViettelPost National Type', default='1')
    receiver_id = fields.Many2one('res.partner', string='Receiver')
    receiver_phone = fields.Char(related='receiver_id.phone', string='Phone')
    receiver_email = fields.Char(related='receiver_id.email', string='Email')
    receiver_street = fields.Char(related='receiver_id.street', string='Street')
    receiver_ward_id = fields.Many2one(related='receiver_id.ward_id', string='Ward')
    receiver_district_id = fields.Many2one(related='receiver_id.district_id', string='District')
    receiver_province_id = fields.Many2one(related='receiver_id.city_id', string='Province')

    sender_id = fields.Many2one('viettelpost.store', string='Sender')
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)

    def action_booking_viettelpost(self):
        ...
