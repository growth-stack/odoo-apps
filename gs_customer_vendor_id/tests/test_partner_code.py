import re

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install', 'gs_customer_vendor_id')
class TestPartnerCode(TransactionCase):

    def test_customer_from_sales_menu(self):
        partner = self.env['res.partner'].with_context(res_partner_search_mode='customer').create(
            {'name': 'Tareli Supermarkets', 'is_company': True})
        self.assertRegex(partner.customer_code, r'^CUS-\d{5}$')
        self.assertFalse(partner.vendor_code)

    def test_vendor_from_purchase_menu(self):
        partner = self.env['res.partner'].with_context(res_partner_search_mode='supplier').create(
            {'name': 'Adera PET Packaging', 'is_company': True})
        self.assertRegex(partner.vendor_code, r'^VEN-\d{5}$')
        self.assertFalse(partner.customer_code)

    def test_plain_contact_gets_id_when_first_used(self):
        partner = self.env['res.partner'].create({'name': 'Walk-in', 'is_company': True})
        self.assertFalse(partner.customer_code)
        partner._increase_rank('customer_rank')
        self.assertRegex(partner.customer_code, r'^CUS-\d{5}$')
        code = partner.customer_code
        partner._increase_rank('supplier_rank')
        self.assertEqual(partner.customer_code, code, "an existing ID never changes")
        self.assertRegex(partner.vendor_code, r'^VEN-\d{5}$')

    def test_ids_are_sequential_and_unique(self):
        Partner = self.env['res.partner'].with_context(res_partner_search_mode='customer')
        a, b = Partner.create([{'name': 'A'}, {'name': 'B'}])
        num = lambda p: int(re.search(r'\d+$', p.customer_code).group())
        self.assertEqual(num(b), num(a) + 1)
        self.assertFalse(a.with_context(res_partner_search_mode=False).copy().customer_code, "a duplicate starts without an ID")

    def test_person_under_company_gets_no_id(self):
        company = self.env['res.partner'].with_context(res_partner_search_mode='customer').create(
            {'name': 'Mavori Hotels', 'is_company': True})
        person = self.env['res.partner'].with_context(res_partner_search_mode='customer').create(
            {'name': 'Ada', 'parent_id': company.id})
        self.assertTrue(company.customer_code)
        self.assertFalse(person.customer_code)

    def test_search_by_id(self):
        partner = self.env['res.partner'].with_context(res_partner_search_mode='customer').create(
            {'name': 'Oseli Catering', 'is_company': True})
        found = self.env['res.partner'].name_search(partner.customer_code)
        self.assertIn(partner.id, [r[0] for r in found])

    def test_posting_invoice_makes_customer(self):
        partner = self.env['res.partner'].create({'name': 'Venari Stores', 'is_company': True})
        if not self.env.company.chart_template:
            self.skipTest("no chart of accounts")
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_line_ids': [(0, 0, {'name': 'Water', 'quantity': 1, 'price_unit': 100})],
        })
        invoice.action_post()
        self.assertRegex(partner.customer_code, r'^CUS-\d{5}$')

    def test_change_prefix_in_settings(self):
        old = self.env['res.partner'].with_context(res_partner_search_mode='supplier').create({'name': 'Old Vendor'})
        settings = self.env['res.config.settings'].create({})
        self.assertEqual(settings.gs_vendor_prefix, 'VEN-')
        settings.gs_vendor_prefix = 'GSVEN-'
        settings.gs_vendor_next = 500
        settings.execute()
        new = self.env['res.partner'].with_context(res_partner_search_mode='supplier').create({'name': 'New Vendor'})
        self.assertEqual(new.vendor_code, 'GSVEN-00500')
        self.assertTrue(old.vendor_code.startswith('VEN-'), "existing IDs keep their prefix")
