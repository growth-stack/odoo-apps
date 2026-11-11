from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _rec_names_search = ('complete_name', 'email', 'ref', 'vat', 'customer_code', 'vendor_code')

    customer_code = fields.Char(
        string="Customer ID", copy=False, readonly=True, index='btree_not_null',
        help="Assigned automatically the first time this contact becomes a customer.")
    vendor_code = fields.Char(
        string="Vendor ID", copy=False, readonly=True, index='btree_not_null',
        help="Assigned automatically the first time this contact becomes a vendor.")

    _sql_constraints = [
        ('customer_code_unique', 'UNIQUE(customer_code)', "This Customer ID is already used by another contact."),
        ('vendor_code_unique', 'UNIQUE(vendor_code)', "This Vendor ID is already used by another contact."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._gs_assign_codes()
        return partners

    def write(self, vals):
        res = super().write(vals)
        if {'customer_rank', 'supplier_rank', 'parent_id'} & set(vals):
            self._gs_assign_codes()
        return res

    def _increase_rank(self, field, n=1):
        # Odoo 18 raises the rank with plain SQL, which skips write()
        super()._increase_rank(field, n)
        if field in ('customer_rank', 'supplier_rank'):
            self._gs_assign_codes()

    def _gs_assign_codes(self):
        """Give a Customer ID / Vendor ID to top-level contacts that are
        customers / vendors and don't have one yet. Never changes an ID."""
        Sequence = self.env['ir.sequence'].sudo()
        for partner in self.sudo().filtered(lambda p: not p.parent_id):
            vals = {}
            if partner.customer_rank > 0 and not partner.customer_code:
                vals['customer_code'] = Sequence.next_by_code('gs.customer.code')
            if partner.supplier_rank > 0 and not partner.vendor_code:
                vals['vendor_code'] = Sequence.next_by_code('gs.vendor.code')
            if vals:
                # Bypass our write() to avoid re-entering this method
                super(ResPartner, partner).write(vals)
