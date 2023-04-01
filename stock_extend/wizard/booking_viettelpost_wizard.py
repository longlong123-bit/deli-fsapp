import requests
from datetime import datetime
from typing import Dict, Any, List, Tuple, Sequence
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons.delivery_viettelpost.models.viettelpost_request import ViettelPostRequest
from odoo.addons.stock_extend.dataclass.delivery_dataclasses import ViettelpostDataclass
from odoo.addons.delivery_book_mgmt.models.delivery_book import DeliveryBook

# class ViettelPostRequestInstance(ViettelPostRequest):
#     def book_ship(self, **kwargs):
#         client = self._set_client()
#         requests.post(url=self.endurl, json=kwargs, headers=headers, timeout=300)


class BookingViettelpostWizard(models.TransientModel):
    _name = 'booking.viettelpost.wizard'
    _description = 'This module fills and confirms info about shipment before creating a bill of lading Viettelpost.'

    deli_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier', required=True, readonly=True)
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
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)
    check_unique = fields.Boolean(string='Check unique', help='Check unique to check SO exists in Viettelpost.')
    note = fields.Text(string='Note')
    product_name = fields.Char(string='Product name', required=True)
    no_of_package = fields.Integer(string='Number of package', required=True, default=1)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    cod = fields.Monetary(string='COD', currency_field='currency_id')
    weight = fields.Float(string='Weight')

    @api.onchange('deli_order_id')
    def _onchange_deli_order_id(self):
        for rec in self:
            if rec.deli_order_id:
                rec.cod = rec.deli_order_id.sale_id.amount_due
                rec.sender_id = rec.deli_order_id.picking_type_id.warehouse_id.id

    @api.onchange('sender_id')
    def _onchange_sender_id(self):
        for rec in self:
            if rec.sender_id:
                rec.sender_phone = rec.sender_id.partner_id.phone
                rec.sender_street = rec.sender_id.partner_id.street
                rec.sender_ward_id = rec.sender_id.partner_id.ward_id.id
                rec.sender_district_id = rec.sender_id.partner_id.district_id.id
                rec.sender_province_id = rec.sender_id.partner_id.city_id.id

    @api.onchange('receiver_id')
    def _onchange_receiver_id(self):
        for rec in self:
            if rec.receiver_id:
                rec.receiver_phone = rec.receiver_id.phone
                rec.receiver_street = rec.receiver_id.street
                rec.receiver_ward_id = rec.receiver_id.ward_id.id
                rec.receiver_district_id = rec.receiver_id.district_id.id
                rec.receiver_province_id = rec.receiver_id.city_id.id

    def _get_address_sender(self) -> str:
        street = self.sender_street or ''
        ward = self.sender_ward_id.name or ''
        district = self.sender_district_id.name or ''
        city = self.sender_province_id.name or ''
        country = self.sender_province_id.country_id.name or ''
        address = ', '.join([el for el in [street, ward, district, city, country] if el])
        return address

    def _get_sender(self) -> Dict[str, Any]:
        partner_id = self.sender_id.partner_id
        sender: dict = {
            'SENDER_FULLNAME': partner_id.name,
            'SENDER_ADDRESS': self._get_address_sender(),
            'SENDER_PHONE': partner_id.phone,
            'SENDER_EMAIL': partner_id.email or '',
            'SENDER_WARD': partner_id.ward_id.viettelpost_wards_id,
            'SENDER_DISTRICT': partner_id.district_id.viettelpost_district_id,
            'SENDER_PROVINCE': partner_id.city_id.viettelpost_province_id,
            'SENDER_LATITUDE': 0,
            'SENDER_LONGITUDE': 0,
        }
        return sender

    def _get_address_receiver(self) -> str:
        street = self.receiver_street or ''
        ward = self.receiver_ward_id.name or ''
        district = self.receiver_district_id.name or ''
        city = self.receiver_province_id.name or ''
        country = self.receiver_province_id.country_id.name or ''
        address = ', '.join([el for el in [street, ward, district, city, country] if el])
        return address

    def _get_receiver(self) -> Dict[str, Any]:
        receiver = {
            'RECEIVER_FULLNAME': self.receiver_id.name,
            'RECEIVER_ADDRESS': self._get_address_receiver(),
            'RECEIVER_PHONE': self.receiver_phone,
            'RECEIVER_EMAIL': self.receiver_id.email or '',
            'RECEIVER_WARD': self.receiver_ward_id.viettelpost_wards_id,
            'RECEIVER_DISTRICT': self.receiver_district_id.viettelpost_district_id,
            'RECEIVER_PROVINCE': self.receiver_province_id.viettelpost_province_id,
            'RECEIVER_LATITUDE': 0,
            'RECEIVER_LONGITUDE': 0,
        }
        return receiver

    def _get_list_item(self) -> Dict[str, List[Dict[str, Any]]]:
        lst_item: dict = {
            'LIST_ITEM': [
                {
                    'PRODUCT_NAME': line.product_id.product_tmpl_id.name,
                    'PRODUCT_PRICE': line.price_subtotal,
                    'PRODUCT_WEIGHT': line.product_id.product_tmpl_id.weight,
                    'PRODUCT_QUANTITY': line.product_uom_qty
                } for line in self.deli_order_id.sale_id.order_line
            ]
        }
        return lst_item

    def _validate_payload(self):
        fields = {
            'Delivery carrier': self.deli_carrier_id,
            'Delivery order': self.deli_order_id,
            'Sender': self.sender_id,
            'Sender Phone': self.sender_phone,
            'Sender Street': self.sender_street,
            'Sender Ward': self.sender_ward_id,
            'Sender District': self.sender_district_id,
            'Sender Province': self.sender_province_id,
            'Store': self.store_id,
            'Service Type': self.service_type,
            'Order Payment': self.order_payment,
            'Product Type': self.product_type,
            'National Type': self.national_type,
            'Product Name': self.product_name,
            'Number of Package': self.no_of_package,
            'Receiver': self.receiver_id,
            'Receiver Phone': self.receiver_phone,
            'Receiver Street': self.receiver_street,
            'Receiver Ward': self.receiver_ward_id,
            'Receiver District': self.receiver_district_id,
            'Receiver Province': self.receiver_province_id,
            'List Item': len(self.deli_order_id.sale_id.order_line)
        }
        for field, value in fields.items():
            if not value:
                raise ValidationError(_(f'The field {field} is required.'))

    def _get_delivery_book_payload(self, dataclass: ViettelpostDataclass) -> Dict[str, Any]:
        payload = {
            'carrier_id': self.deli_carrier_id.id,
            'service_type': self.service_type,
            'order_payment': self.order_payment,
            'product_type': self.product_type,
            'national_type': self.national_type,
            'receiver_id': self.receiver_id.id,
            'receiver_phone': self.receiver_phone,
            'receiver_street': self.receiver_street,
            'receiver_ward_id': self.receiver_ward_id.id,
            'receiver_district_id': self.receiver_district_id.id,
            'receiver_province_id': self.receiver_province_id.id,
            'store_id': self.store_id.id,
            'sender_id': self.sender_id.id,
            'sender_phone': self.sender_phone,
            'sender_street': self.sender_street,
            'sender_ward_id': self.sender_ward_id.id,
            'sender_district_id': self.sender_district_id.id,
            'sender_province_id': self.sender_province_id.id,
            'deli_order_id': self.deli_order_id.id,
            'note': self.note,
            'num_of_package': self.no_of_package,
            'fee_ship': dataclass.money_total_fee,
            'money_total': dataclass.money_total,
            'money_fee': dataclass.money_fee,
            'money_collection_fee': dataclass.money_collection_fee,
            'money_vat': dataclass.money_vat,
            'money_other_fee': dataclass.money_other_fee,
            'bl_code': dataclass.bl_code,
            'cod': dataclass.money_collection,
            'weight': dataclass.exchange_weight,
            'est_deli_time': dataclass.kpi_ht,
            'tracking_link': f'https://viettelpost.vn/thong-tin-don-hang?peopleTracking=sender&orderNumber=17706321127',
            'state': 'Giao cho buu ta di nhan',
        }
        return payload

    def action_booking_viettelpost(self):
        self._validate_payload()
        payload = {
            'ORDER_NUMBER': self.deli_order_id.name,
            'GROUPADDRESS_ID': self.store_id.group_address_id,
            'CUS_ID': self.store_id.customer_id,
            'DELIVERY_DATE': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'PRODUCT_NAME': self.product_name,
            'PRODUCT_QUANTITY': self.no_of_package,
            'PRODUCT_PRICE': self.deli_order_id.sale_id.amount_total,
            'PRODUCT_WEIGHT': self.weight,
            'ORDER_NOTE': self.note,
            'MONEY_COLLECTION': self.cod,
            'PRODUCT_TYPE': self.product_type,
            'ORDER_PAYMENT': int(self.order_payment),
            'ORDER_SERVICE': self.service_type
        }
        sender = self._get_sender()
        receiver = self._get_receiver()
        lst_item = self._get_list_item()
        payload = {**payload, **sender, **receiver, **lst_item}
        if self.check_unique:
            payload = {**payload, **{'CHECK_UNIQUE': True}}
        result = {
                "ORDER_NUMBER": "17706321127",
                "MONEY_COLLECTION": 0,
                "EXCHANGE_WEIGHT": 50,
                "MONEY_TOTAL": 11000,
                "MONEY_TOTAL_FEE": 10000,
                "MONEY_FEE": 0,
                "MONEY_COLLECTION_FEE": 0,
                "MONEY_OTHER_FEE": 0,
                "MONEY_VAS": 0,
                "MONEY_VAT": 1000,
                "KPI_HT": 24.0,
                "RECEIVER_PROVINCE": 2,
                "RECEIVER_DISTRICT": 35,
                "RECEIVER_WARDS": 672
            }
        dataclass_vtp = ViettelpostDataclass(*ViettelpostDataclass.load_data(result))
        delivery_book_payload = self._get_delivery_book_payload(dataclass_vtp)
        self.env['delivery.book'].sudo().create(delivery_book_payload)

