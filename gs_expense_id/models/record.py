from odoo import api, fields, models


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    expense_code = fields.Char(
        string="Expense ID", copy=False, readonly=True, index='btree_not_null',
        help="Assigned automatically when the record is created. It never changes.")

    _expense_code_unique = models.Constraint(
        'UNIQUE(expense_code)', "This Expense ID is already used.")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._gs_assign_expense_code()
        return records

    def _gs_assign_expense_code(self):
        """Give an ID to the records that don't have one yet. Never changes an ID."""
        Sequence = self.env['ir.sequence'].sudo()
        for record in self.sudo().filtered(lambda r: not r.expense_code).sorted('id'):
            record.expense_code = Sequence.next_by_code('gs.expense.code')
