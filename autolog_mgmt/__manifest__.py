{
    'name': 'Autologistics',
    'version': '17.0.1.0.0',
    'author': 'Sasha Lytvychenko',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/autolog_receive_car_views.xml',
        'views/autolog_repair_car_views.xml',
        'views/autolog_repair_car_service_views.xml',
        'views/autolog_truck_driver_views.xml',
        'views/autolog_car_brands_views.xml',
        'views/autolog_car_dealer_views.xml',
        'views/menu_views.xml',
        'report/autolog_receive_car_report.xml',


    ],
    'demo': [


    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ]
}
