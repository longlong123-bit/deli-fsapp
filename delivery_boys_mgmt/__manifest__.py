{
    'name': 'Delivery Boys Management',
    'version': '14.0.1.0',
    'summary': 'Module to manage deliveries by home driver',
    'description': """""",
    'category': 'Inventory/Delivery',
    'support': 'odoo.tangerine@gmail.com',
    'author': 'Tangerine',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'viettelpost_address', 'stock_extend', 'contacts', 'stock', 'sale', 'delivery'],
    'data': [
        'security/deli_boys_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/cancel_delivery_boys_wizard_views.xml',
        'wizard/complete_delivery_wizard_views.xml',
        'views/delivery_boys_views.xml',
        'views/menus.xml',
    ],
    'application': True
}