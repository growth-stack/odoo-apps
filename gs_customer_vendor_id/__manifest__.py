{
    'name': 'Customer and Vendor IDs',
    'version': '20.0.1.0.2',
    'summary': 'Give every customer and vendor a permanent, searchable ID (CUS-00001, VEN-00001) with your own prefix',
    'description': """
Gives every customer and vendor a permanent ID:

* Customer ID, e.g. CUS-00001, assigned the first time a contact becomes a
  customer (created from Sales > Customers, or used on a confirmed sale or
  posted invoice)
* Vendor ID, e.g. VEN-00001, assigned the same way for vendors
* A contact that is both gets both IDs
* IDs show on the contact form and list, and you can search contacts,
  quotations, orders and invoices by them
* Existing customers and vendors get IDs when the module is installed

Only the company (or individual) gets an ID, not the people listed under it.
Change the prefix (e.g. VEN- to GSVEN-) and next number under
Invoicing/Accounting > Configuration > Settings > Customer and Vendor IDs.
New IDs use the new prefix; existing IDs never change.
""",
    'category': 'Sales/Sales',
    'author': 'Growth Stack',
    'maintainer': 'Growth Stack',
    'website': 'https://www.growthstack.gs',
    'support': 'help@growthstack.gs',
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'depends': ['account'],
    'data': [
        'data/ir_sequence.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
