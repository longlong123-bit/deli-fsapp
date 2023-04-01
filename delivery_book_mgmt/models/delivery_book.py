from typing import List, Tuple

from odoo import models, fields, _


class DeliveryBook(models.Model):
    _name = 'delivery.book'
    _inherit = ['mail.thread']
    _rec_name = 'bl_code'
    _description = 'Manage deliveries by home shipper'

    @staticmethod
    def get_viettelpost_service_types() -> List[Tuple]:
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
    def viettelpost_order_payments() -> List[Tuple]:
        return [('1', _('Uncollect money')),
                ('2', _('Collect express fee and price of goods.')),
                ('3', _('Collect price of goods')),
                ('4', _('Collect express fee'))]

    @staticmethod
    def viettelpost_product_types() -> List[Tuple]:
        return [('TH', 'Envelope'), ('HH', 'Goods')]

    @staticmethod
    def viettelpost_national_types() -> List[Tuple]:
        return [('1', 'Inland'), ('0', 'International')]

    carrier_id = fields.Many2one('delivery.carrier', string='Shipping method', required=True, tracking=True)
    carrier_type = fields.Selection(related='carrier_id.delivery_type')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    # fields for viettelpost
    service_type = fields.Selection(
        selection=lambda self: DeliveryBook.get_viettelpost_service_types(),
        string='Service Type', default='VCN', required=True)
    order_payment = fields.Selection(selection=lambda self: DeliveryBook.viettelpost_order_payments(),
                                     string='Order Payment', default='1', required=True)
    product_type = fields.Selection(selection=lambda self: DeliveryBook.viettelpost_product_types(),
                                    string='Product Type', default='HH', required=True)
    national_type = fields.Selection(selection=lambda self: DeliveryBook.viettelpost_national_types(),
                                     string='National Type', default='1', required=True)

    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True)
    receiver_phone = fields.Char(string='Phone', required=True)
    receiver_street = fields.Char(string='Street', required=True)
    receiver_ward_id = fields.Many2one('res.ward', string='Ward', required=True)
    receiver_district_id = fields.Many2one('res.district', string='District', required=True)
    receiver_province_id = fields.Many2one('res.city', string='Province', required=True)

    sender_id = fields.Many2one('stock.warehouse', string='Sender', required=True)
    sender_phone = fields.Char(string='Phone', required=True)
    sender_street = fields.Char(string='Address', required=True)
    sender_ward_id = fields.Many2one('res.ward', string='Ward', required=True)
    sender_district_id = fields.Many2one('res.district', string='District', required=True)
    sender_province_id = fields.Many2one('res.city', string='Province', required=True)

    store_id = fields.Many2one('viettelpost.store', string='Store', required=True)

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
    tracking_link = fields.Char(string='Tracking link')
    money_total = fields.Monetary(string='Money total', readonly=True, currency_field='currency_id')
    money_fee = fields.Monetary(string='Money fee', readonly=True, currency_field='currency_id')
    money_collection_fee = fields.Monetary(string='Money collection fee', readonly=True,
                                           currency_field='currency_id')
    money_vat = fields.Monetary(string='Money VAT', readonly=True, currency_field='currency_id')
    money_other_fee = fields.Monetary(string='Money other fee', readonly=True, currency_field='currency_id')