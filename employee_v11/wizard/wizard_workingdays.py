from odoo import models, fields, api
from odoo.osv import osv


class wizartWorkingDays(osv.TransientModel):
    _name = "wizard.working.days"
    _description = "Working Days Calculation"

    days = fields.Float(string="Working Days", _default=30)

    def do_calc(self, context=None):
        emp_record = self.env["employee"].browse(context.get("active_ids"))
        calculated_salary = (emp_record.basic) - ((emp_record.basic / self.days) * emp_record.leaves)
        emp_record.write({'testtotal': calculated_salary})
        return True
