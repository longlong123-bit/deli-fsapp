from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BookingAhamoveWizard(models.TransientModel):
    _name = 'booking.ahamove.wizard'

    @staticmethod
    def get_ahamove_service_types():
        return [
            ('SGN-BIKE', 'Sai Gon Bike'),
            ('HAN-BIKE', 'Ha Noi Bike'),
            ('VCA-BIKE', 'Can Tho Bike'),
            ('DAD-BIKE', 'Da Nang Bike'),
            ('SGN-VAN-1000', 'Sai Gon VAN1000'),
            ('HAN-VAN-1000', 'Ha Noi VAN1000')
        ]

    @staticmethod
    def get_payment_method():
        return [('online', 'Online'), ('cod', 'Cod')]

    @staticmethod
    def get_payment():
        return [('CASH', 'CASH'), ('BALANCE', 'BALANCE')]

    @staticmethod
    def get_merchandises():
        return [
            ('TIER_1', 'Tiêu chuẩn'),
            ('TIER_2', 'Mức 1'),
            ('TIER_3', 'Mức 2'),
            ('TIER_4', 'Mức 3')
        ]

    deli_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier', required=True, readonly=True)
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    service_type = fields.Selection(
        selection=lambda self: BookingAhamoveWizard.get_ahamove_service_types(),
        string='Service Type', default='SGN-BIKE', required=True)
    payment_method = fields.Selection(selection=lambda self: BookingAhamoveWizard.get_payment_method(),
                                      string='Payment Method', default='online', required=True)
    payment = fields.Selection(selection=lambda self: BookingAhamoveWizard.get_payment(), string='Thanh toán',
                               default='CASH', required=True)

    merchandises = fields.Selection(selection=lambda self: BookingAhamoveWizard.get_merchandises(),
                                    default='TIER_1', required=True)
    note = fields.Text(string='Note')
    is_back = fields.Boolean(string='Back to pick up point')
    cod = fields.Integer(string='COD')
    weight = fields.Float(string='Weight')
    no_of_package = fields.Integer(string='Number of package', required=True)

    warehouse_id = fields.Many2one('stock.warehouse', string='Sender', required=True)
    sender_id = fields.Many2one('res.partner', string='Sender', required=True)
    sender_phone = fields.Char(string='Phone', required=True)
    sender_street = fields.Char(string='Address', required=True)
    sender_ward_id = fields.Many2one('res.ward', string='Ward', required=True)
    sender_district_id = fields.Many2one('res.district', string='District', required=True)
    sender_province_id = fields.Many2one('res.city', string='Province', required=True)

    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True)
    receiver_phone = fields.Char(string='Phone', required=True)
    receiver_street = fields.Char(string='Street', required=True)
    receiver_ward_id = fields.Many2one('res.ward', string='Ward', required=True)
    receiver_district_id = fields.Many2one('res.district', string='District', required=True)
    receiver_province_id = fields.Many2one('res.city', string='Province', required=True)

    def _validate_ahamove_shipment(self):
        token = self.env.user.company_id.token_aha
        if not token:
            raise UserError(_("Please register to get tokens on ahamove!"))
        elif not self.service_type:
            raise UserError(_('The field service type is required.'))
        elif not self.self.payment_method:
            raise UserError(_('The field payment method is required.'))
        elif not self.warehouse_id:
            raise UserError(_("The field warehouse is required."))
        elif not self.sender_id:
            raise UserError(_("The field sender is required."))
        elif not self.sender_phone:
            raise UserError(_("The field sender phone is required."))
        elif not self.sender_street:
            raise UserError(_("The field sender street is required."))
        elif not self.sender_ward_id:
            raise UserError(_("The field sender ward is required."))
        elif not self.sender_district_id:
            raise UserError(_("The field sender district is required."))
        elif not self.sender_province_id:
            raise UserError(_("The field sender province is required."))
        elif not self.receiver_id:
            raise UserError(_("The field receiver is required."))
        elif not self.receiver_phone:
            raise UserError(_("The field receiver phone is required."))
        elif not self.receiver_street:
            raise UserError(_("The field receiver street is required."))
        elif not self.receiver_ward_id:
            raise UserError(_("The field receiver ward is required."))
        elif not self.receiver_district_id:
            raise UserError(_("The field receiver district is required."))
        elif not self.receiver_province_id:
            raise UserError(_("The field receiver province is required."))
        elif not self.receiver_province_id:
            raise UserError(_("The field receiver province is required."))
        elif not self.payment:
            raise UserError(_("The field payment is required."))
        elif not self.merchandises:
            raise UserError(_("The field merchandises is required."))
        elif not self.no_of_package:
            raise UserError(_("The field number of package is required."))
        return token

    def _get_address_sender(self) -> str:
        street = self.sender_street or ''
        ward = self.sender_ward_id.name or ''
        district = self.sender_district_id.name or ''
        city = self.sender_province_id.name or ''
        country = self.sender_province_id.country_id.name or ''
        address = ', '.join([el for el in [street, ward, district, city, country] if el])
        return address

    def action_booking_ahamove(self):
        base_url = 'https://api.ahamove.com/v1/order/create?token='
        self._validate_ahamove_shipment()
        sender_address = self._get_address_sender()
        rail = f'&service_id={self.service_type}&requests=[]&payment_method={self.payment_method}'
        add_sender = f'"address":"{sender_address}","mobile":"{self.sender_phone}'
