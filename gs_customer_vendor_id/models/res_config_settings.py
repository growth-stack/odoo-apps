from odoo import api, fields, models

SEQUENCES = {
    'customer': 'gs_customer_vendor_id.seq_customer_code',
    'vendor': 'gs_customer_vendor_id.seq_vendor_code',
}


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gs_customer_prefix = fields.Char("Customer ID prefix")
    gs_customer_next = fields.Integer("Next customer number")
    gs_vendor_prefix = fields.Char("Vendor ID prefix")
    gs_vendor_next = fields.Integer("Next vendor number")

    def _gs_sequence(self, kind):
        return self.env.ref(SEQUENCES[kind], raise_if_not_found=False)

    @api.model
    def get_values(self):
        res = super().get_values()
        for kind in SEQUENCES:
            seq = self._gs_sequence(kind)
            if seq:
                res[f'gs_{kind}_prefix'] = seq.prefix
                res[f'gs_{kind}_next'] = seq.number_next_actual
        return res

    def set_values(self):
        super().set_values()
        for kind in SEQUENCES:
            seq = self._gs_sequence(kind)
            if not seq:
                continue
            vals = {}
            prefix = self[f'gs_{kind}_prefix'] or ''
            if prefix != (seq.prefix or ''):
                vals['prefix'] = prefix
            next_number = self[f'gs_{kind}_next']
            if next_number and next_number != seq.number_next_actual:
                vals['number_next_actual'] = next_number
            if vals:
                seq.sudo().write(vals)
