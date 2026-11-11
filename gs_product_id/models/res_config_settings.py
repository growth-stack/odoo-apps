from odoo import api, fields, models

SEQUENCE = 'gs_product_id.seq_product_code'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gs_product_prefix = fields.Char("Product ID prefix")
    gs_product_next = fields.Integer("Next product number")

    @api.model
    def get_values(self):
        res = super().get_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if seq:
            res['gs_product_prefix'] = seq.prefix
            res['gs_product_next'] = seq.number_next_actual
        return res

    def set_values(self):
        super().set_values()
        seq = self.env.ref(SEQUENCE, raise_if_not_found=False)
        if not seq:
            return
        vals = {}
        prefix = self.gs_product_prefix or ''
        if prefix != (seq.prefix or ''):
            vals['prefix'] = prefix
        if self.gs_product_next and self.gs_product_next != seq.number_next_actual:
            vals['number_next_actual'] = self.gs_product_next
        if vals:
            seq.sudo().write(vals)
