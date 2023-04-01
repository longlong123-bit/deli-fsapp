{
    'name': 'Delivery Boys Management',
    'version': '14.0.1.0',
    'summary': 'Module to manage deliveries by home driver',
    'description': """""",
    'category': 'Inventory/Delivery',
    'support': 'odoo.tangerine@gmail.com',
    'author': 'Tangerine',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'viettelpost_address', 'contacts', 'stock', 'sale', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/delivery_boys_views.xml',
        'wizard/complete_delivery_wizard.xml',
        'wizard/cancel_delivery_wizard.xml',
        'views/menus.xml',
    ],
    'application': True
}