from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductCode(TransactionCase):

    def test_new_product_gets_reference(self):
        template = self.env['product.template'].create({'name': 'Mug'})
        self.assertTrue(template.default_code.startswith('PRD-'))
        self.assertEqual(template.product_variant_id.default_code, template.default_code)

    def test_typed_reference_is_kept(self):
        template = self.env['product.template'].create({'name': 'Cap', 'default_code': 'MY-CAP'})
        self.assertEqual(template.default_code, 'MY-CAP')
        product = self.env['product.product'].create({'name': 'Hat', 'default_code': 'MY-HAT'})
        self.assertEqual(product.default_code, 'MY-HAT')

    def test_each_variant_gets_its_own_reference(self):
        attribute = self.env['product.attribute'].create({
            'name': 'Size', 'value_ids': [(0, 0, {'name': 'S'}), (0, 0, {'name': 'L'})],
        })
        template = self.env['product.template'].create({
            'name': 'Shirt',
            'attribute_line_ids': [(0, 0, {
                'attribute_id': attribute.id, 'value_ids': [(6, 0, attribute.value_ids.ids)],
            })],
        })
        codes = template.product_variant_ids.mapped('default_code')
        self.assertEqual(len(codes), 2)
        self.assertEqual(len(set(codes)), 2)
        self.assertTrue(all(code.startswith('PRD-') for code in codes))

    def test_duplicate_gets_new_reference(self):
        template = self.env['product.template'].create({'name': 'Pen'})
        copy = template.copy()
        self.assertTrue(copy.default_code)
        self.assertNotEqual(copy.default_code, template.default_code)

    def test_settings_change_prefix(self):
        settings = Form(self.env['res.config.settings'])
        self.assertEqual(settings.gs_product_prefix, 'PRD-')
        settings.gs_product_prefix = 'SKU-'
        settings.gs_product_next = 1000
        settings.save().execute()
        self.assertEqual(self.env['product.product'].create({'name': 'Lamp'}).default_code, 'SKU-01000')
