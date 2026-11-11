from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestExpenseCode(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env['hr.employee'].create({'name': 'Expense Tester'})
        cls.product = cls.env['product.product'].create({
            'name': 'Taxi', 'type': 'service', 'can_be_expensed': True, 'standard_price': 0,
        })

    def _expense(self, name='Taxi to client'):
        return self.env['hr.expense'].create({
            'name': name, 'employee_id': self.employee.id, 'product_id': self.product.id,
            'total_amount_currency': 25,
        })

    def test_new_expense_gets_id(self):
        first, second = self._expense(), self._expense('Lunch')
        self.assertTrue(first.expense_code.startswith('EXP-'))
        self.assertNotEqual(first.expense_code, second.expense_code)

    def test_existing_expenses_have_ids(self):
        self.assertFalse(self.env['hr.expense'].search([('expense_code', '=', False)]))

    def test_id_is_kept_and_not_copied(self):
        expense = self._expense()
        code = expense.expense_code
        expense.name = 'Taxi to the airport'
        self.assertEqual(expense.expense_code, code)
        copy = expense.copy()
        self.assertTrue(copy.expense_code)
        self.assertNotEqual(copy.expense_code, code)

    def test_settings_change_prefix(self):
        settings = Form(self.env['res.config.settings'])
        self.assertEqual(settings.gs_expense_prefix, 'EXP-')
        settings.gs_expense_prefix = 'CLAIM-'
        settings.gs_expense_next = 42
        settings.save().execute()
        self.assertEqual(self._expense().expense_code, 'CLAIM-00042')
