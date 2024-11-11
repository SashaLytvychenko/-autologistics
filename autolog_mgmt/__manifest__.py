{
    'name': 'Autologistics',
    'version': '17.0.1.0.0',
    'author': 'Sasha Lytvychenko',
    'summary': 'Manage vehicle logistics, repairs, dealers, and drivers'
               ' efficiently',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail',
        'stock',
        'sale_management',
    ],
    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/autolog_groups.xml',
        'security/ir.model.access.csv',
        'security/autolog_security.xml',
        'data/sequence.xml',
        'wizard/autolog_car_wizard_views.xml',
        'views/autolog_receive_car_views.xml',
        'views/autolog_repair_car_views.xml',
        'views/autolog_truck_driver_views.xml',
        'views/autolog_car_brands_views.xml',
        'views/autolog_car_dealer_views.xml',
        'views/menu_views.xml',
        'report/autolog_receive_car_report.xml',

    ],
    'demo': [
        'demo/product.product.csv',
        'demo/autolog_truck_driver_demo.xml',
        'demo/autolog_car_brands_demo.xml',
        'demo/autolog_car_dealer_demo.xml',
        'demo/autolog_receive_car_demo.xml',
        'demo/autolog_repair_car_demo.xml',

    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ]
}
