from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_code = fields.Char(
        string="Employee ID", copy=False, readonly=True, index='btree_not_null',
        help="Assigned automatically when the record is created. It never changes.")

    _employee_code_unique = models.Constraint(
        'UNIQUE(employee_code)', "This Employee ID is already used.")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._gs_assign_employee_code()
        return records

    def _gs_assign_employee_code(self):
        """Give an ID to the records that don't have one yet. Never changes an ID."""
        Sequence = self.env['ir.sequence'].sudo()
        for record in self.sudo().filtered(lambda r: not r.employee_code).sorted('id'):
            record.employee_code = Sequence.next_by_code('gs.employee.code')
