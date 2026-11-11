def post_init_hook(env):
    """Give existing records their IDs, oldest first."""
    records = env['hr.employee'].with_context(active_test=False).search([], order='id')
    records._gs_assign_employee_code()
