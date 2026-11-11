from odoo import api, fields, models

SEQUENCE = 'gs_expense_id.seq_expense_code'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gs_expense_prefix = fields.Char("Expense ID prefix")
    gs_expense_next = fields.Integer("Next expense number")

    @api.model
    def get_values(self):
        res = super().get_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if seq:
            res['gs_expense_prefix'] = seq.prefix
            res['gs_expense_next'] = seq.number_next_actual
        return res

    def set_values(self):
        super().set_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if not seq:
            return
        vals = {}
        prefix = self.gs_expense_prefix or ''
        if prefix != (seq.prefix or ''):
            vals['prefix'] = prefix
        if self.gs_expense_next and self.gs_expense_next != seq.number_next_actual:
            vals['number_next_actual'] = self.gs_expense_next
        if vals:
            seq.sudo().write(vals)
