def post_init_hook(env):
    """Give existing customers and vendors their IDs."""
    partners = env['res.partner'].with_context(active_test=False).search([
        ('parent_id', '=', False),
        '|', ('customer_rank', '>', 0), ('supplier_rank', '>', 0),
    ], order='id')
    partners._gs_assign_codes()
