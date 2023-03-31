from odoo import models, fields, api, _
from odoo.addons.delivery_viettelpost.models.viettelpost_request import ViettelPostRequest


class BookingViettelpostWizard(models.TransientModel):
    _name = 'booking.viettelpost.wizard'
    _description = 'This module fills and confirms info about shipment before creating a bill of lading Viettelpost.'

    @staticmethod
    def get_viettelpost_service_types():
        return [
            ('VCN', 'Tài liệu nhanh'),
            ('V24', 'Đồng giá 24K'),
            ('LECO', 'Hàng nặng tiết kiệm'),
            ('VTK', 'Tài liệu tiết kiệm'),
            ('V60', 'V60 Dịch vụ Nhanh 60h'),
            ('VHT', 'Hỏa tốc, hẹn giờ'),
            ('NCOD', 'Chuyển phát nhanh'),
            ('SCOD', 'SCOD Giao hàng thu tiền'),
            ('PTN', 'Nội tỉnh nhanh'),
            ('V25', 'V25'),
            ('V30', 'V30'),
            ('V20', 'V20'),
            ('PHS', 'Nội tỉnh tiết kiệm'),
            ('V35', 'V35'),
            ('VBS', 'VBS Nhanh theo hộp'),
            ('V02', 'TMDT Phát nhanh 2h'),
            ('VBE', 'VBE Tiết kiệm theo hộp'),
            ('LCOD', 'Chuyển phát tiêu chuẩn'),
            ('ECOD', 'ECOD Giao hành thu tiền tiết kiệm'),
            ('LSTD', 'Hàng nặng nhanh'),
            ('VCBA', 'Chuyển phát đường bay'),
            ('VCBO', 'Chuyển phát đường bộ'),
            ('V505', 'Dịch vụ 5+ gói 500g'),
            ('V510', 'Dịch vụ 5+ gói 1000g'),
            ('V520', 'Dịch vụ 5+ gói 2000g'),
            ('PTTT', 'Phân tích thị trường'),
            ('V510', 'Dịch vụ 5+ gói 1000g'),
            ('V02', 'TMDT Phát nhanh 2h'),
            ('V520', 'Dịch vụ 5+ gói 2000g'),
            ('VCBO', 'Chuyển phát đường bộ'),
            ('VCBA', 'Chuyển phát đường bay'),
            ('LSTD', 'Hàng nặng nhanh'),
            ('V505', 'Dịch vụ 5+ gói 500g'),
            ('PTTT', 'Phân tích thị trường'),
            ('NCOD', 'Chuyển phát nhanh'),
            ('SCOD', 'SCOD Giao hàng thu tiền'),
            ('PTN', 'Nội tỉnh nhanh'),
            ('V30', 'V30'),
            ('V25', 'V25'),
            ('PHS', 'Nội tỉnh tiết kiệm'),
            ('V20', 'V20'),
            ('V35', 'V35'),
            ('VCN', 'Tài liệu nhanh'),
            ('V24', 'Đồng giá 24K'),
            ('LECO', 'Hàng nặng tiết kiệm'),
            ('VTK', 'Tài liệu tiết kiệm'),
            ('V60', 'V60 Dịch vụ Nhanh 60h'),
            ('VHT', 'Hỏa tốc, hẹn giờ'),
            ('VBS', 'VBS Nhanh theo hộp'),
            ('VBE', 'VBE Tiết kiệm theo hộp'),
            ('LCOD', 'Chuyển phát tiêu chuẩn'),
            ('ECOD', 'ECOD Giao hành thu tiền tiết kiệm'),
            ('DHC', 'DHL Chuyển phát quốc tế'),
            ('UPS', 'UPS quốc tế chỉ định'),
            ('VQN', 'VQN Quốc tế nhanh'),
            ('VQE', 'VQE Quốc tế chuyên tuyến'),
            ('VVC', 'VVC Giao voucher thu tiền'),
            ('VCT', 'VCT Chuyển tiền nhận tại địa chỉ'),
        ]

    @staticmethod
    def viettelpost_order_payments():
        return [('1', _('Uncollect money')), ('2', _('Collect express fee and price of goods.')), ('3', _('Collect price of goods')), ('4', _('Collect express fee'))]

    @staticmethod
    def viettelpost_product_types():
        return [('TH', 'Envelope'), ('HH', 'Goods')]

    @staticmethod
    def viettelpost_national_types():
        return [('1', 'Inland'), ('0', 'International')]

    deli_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier', required=True, readonly=True)
    service_type = fields.Selection(
        selection=lambda self: BookingViettelpostWizard.get_viettelpost_service_types(),
        string='Service Type', default='VCN', required=True)
    order_payment = fields.Selection(selection=lambda self: BookingViettelpostWizard.viettelpost_order_payments(),
                                     string='Order Payment', default='1', required=True)
    product_type = fields.Selection(selection=lambda self: BookingViettelpostWizard.viettelpost_product_types(),
                                    string='Product Type', default='HH', required=True)
    national_type = fields.Selection(selection=lambda self: BookingViettelpostWizard.viettelpost_national_types(),
                                     string='National Type', default='1', required=True)
    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True)
    receiver_phone = fields.Char(related='receiver_id.phone', string='Phone')
    receiver_street = fields.Char(related='receiver_id.street', string='Street')
    receiver_ward_id = fields.Many2one(related='receiver_id.ward_id', string='Ward')
    receiver_district_id = fields.Many2one(related='receiver_id.district_id', string='District')
    receiver_province_id = fields.Many2one(related='receiver_id.city_id', string='Province')

    sender_id = fields.Many2one('viettelpost.store', string='Sender', required=True)
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)
    deli_date = fields.Datetime(string='Delivery Date', default=lambda self: fields.Datetime.now(), required=True)
    check_unique = fields.Boolean(string='Check unique', help='Check unique to check SO exists in Viettelpost.')
    note = fields.Text(string='Note')

    def action_booking_viettelpost(self):
        ...
