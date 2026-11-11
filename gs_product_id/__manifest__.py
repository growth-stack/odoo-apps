{
    'name': 'Product IDs',
    'version': '20.0.1.0.0',
    'summary': 'Fill every product Internal Reference automatically (PRD-00001) with your own prefix',
    'category': 'Inventory/Products',
    'author': 'Growth Stack',
    'maintainer': 'Growth Stack',
    'website': 'https://github.com/growth-stack',
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'depends': ['product'],
    'data': [
        'data/ir_sequence.xml',
        'views/res_config_settings_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
