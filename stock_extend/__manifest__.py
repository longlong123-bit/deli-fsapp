{
    'name': 'Stock Extend',
    'version': '14.0.1.0',
    'summary': 'This module is used for open wizard handle assign delivery carrier',
    'description': """""",
    'category': 'Inventory/Delivery',
    'support': 'odoo.tangerine@gmail.com',
    'author': 'Tangerine',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'mail', 'stock', 'delivery_boys_mgmt', 'delivery_book_mgmt', 'tr_connect_ahamove', 'delivery_viettelpost'],
    'data': [
        'security/ir.model.access.csv',
        'data/delivery_carrier_data.xml',
        'wizard/booking_viettelpost_wizard_views.xml',
        'wizard/select_deli_carrier_wizard_views.xml',
        'wizard/booking_delivery_boys_wizard.xml',
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
    ],
    'application': True
}