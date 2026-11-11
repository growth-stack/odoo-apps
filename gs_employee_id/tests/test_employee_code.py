from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEmployeeCode(TransactionCase):

    def test_new_employee_gets_id(self):
        first = self.env['hr.employee'].create({'name': 'Ada'})
        second = self.env['hr.employee'].create({'name': 'Grace'})
        self.assertTrue(first.employee_code.startswith('EMP-'))
        self.assertNotEqual(first.employee_code, second.employee_code)

    def test_existing_employees_have_ids(self):
        self.assertFalse(self.env['hr.employee'].with_context(active_test=False).search(
            [('employee_code', '=', False)]))

    def test_id_is_kept(self):
        employee = self.env['hr.employee'].create({'name': 'Linus'})
        code = employee.employee_code
        employee.write({'name': 'Linus T.', 'job_title': 'Engineer'})
        self.assertEqual(employee.employee_code, code)
        self.assertFalse(employee._fields['employee_code'].copy)

    def test_search_by_id(self):
        employee = self.env['hr.employee'].create({'name': 'Margaret'})
        self.assertEqual(self.env['hr.employee'].search([('employee_code', '=', employee.employee_code)]), employee)

    def test_settings_change_prefix(self):
        settings = Form(self.env['res.config.settings'])
        self.assertEqual(settings.gs_employee_prefix, 'EMP-')
        settings.gs_employee_prefix = 'STAFF-'
        settings.gs_employee_next = 200
        settings.save().execute()
        employee = self.env['hr.employee'].create({'name': 'Katherine'})
        self.assertEqual(employee.employee_code, 'STAFF-00200')
