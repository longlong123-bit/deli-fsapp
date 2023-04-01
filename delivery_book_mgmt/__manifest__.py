{
    'name': 'Delivery Carrier Book Management',
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
        'views/delivery_book_views.xml',
        'views/menus.xml'
    ],
    'application': True
}