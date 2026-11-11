from odoo import api, fields, models

SEQUENCE = 'gs_employee_id.seq_employee_code'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gs_employee_prefix = fields.Char("Employee ID prefix")
    gs_employee_next = fields.Integer("Next employee number")

    @api.model
    def get_values(self):
        res = super().get_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if seq:
            res['gs_employee_prefix'] = seq.prefix
            res['gs_employee_next'] = seq.number_next_actual
        return res

    def set_values(self):
        super().set_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if not seq:
            return
        vals = {}
        prefix = self.gs_employee_prefix or ''
        if prefix != (seq.prefix or ''):
            vals['prefix'] = prefix
        if self.gs_employee_next and self.gs_employee_next != seq.number_next_actual:
            vals['number_next_actual'] = self.gs_employee_next
        if vals:
            seq.sudo().write(vals)
