from odoo import models, fields, api
from odoo.exceptions import except_orm


class employee(models.Model):
    _name = "employee"
    _description = "Employee details"
    _rec_name = "emp_id"

    emp_id = fields.Char("Employee ID")
    name = fields.Char(string="Name", required=True)
    image = fields.Binary("Image")
    age = fields.Integer(string="Age")
    active = fields.Boolean(string="Active", default=1)
    basic = fields.Float(string="Basic")
    testtotal = fields.Float(string="Test Total")
    bdate = fields.Datetime(string="Birth date")
    jdate = fields.Date(string="join Date")
    ldate = fields.Date(string="Last Date")
    notes = fields.Text(string="Notes")
    template = fields.Html(string="Template")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], "Gender", default="male")

    department_id = fields.Many2one("department.employee", "Department")
    res_ids = fields.One2many('reference.detail', "employee_id", 'References')
    hobbies_id = fields.Many2many("hobbies.detail", 'employee_hobbie_rel', "emp_id", "hobby_id", 'Hobbies Detail')
    responsible_id = fields.Many2one("res.partner", "Responsible Person")
    email = fields.Char(related='responsible_id.email', string='Resp Email')
    phone = fields.Char(related='responsible_id.phone', string='Resp Contact')
    ref = fields.Reference(selection=[('res.partner', 'Partner'), ('res.users', 'User')])
    ref_link = fields.Char("External Link")
    type = fields.Selection([('trainee', 'Trainee'), ('probation', 'Probation')], 'Employee Type')

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"].next_by_code('employee') or 'New'
        vals['emp_id'] = seq

        return super(employee, self).create(vals)

    # @api.multi
    # def set_emp_sequence(self):
    #     for emp in self:
    #         next_seq = self.env['ir.sequence'].get('employee.code.sequence')
    #         next_seq = "/"
    #         if emp.department_id:
    #             next_seq += emp.department_id.code
    #         emp.emp_id = next_seq
    #     return True

    @api.multi
    def call_wizard(self):
        # return self.env.ref('employee_v11.action_view_form_workingdays').read()[0]
        wizard_form = self.env.ref('employee_v11.view_form_workingdays', False)
        view_id = self.env['wizard.working.days']
        vals = {'days': '30.00',}
        new = view_id.create(vals)
        return {
            'name': ('Work Days'),
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.working.days',
            'res_id': new.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }


    @api.one
    @api.depends('basic', 'leaves')
    def _compute_total(self):
        salary = self.basic - ((self.basic / 30) * self.leaves)
        self.total = salary

    total = fields.Float(string='Salary', store=True, readonly=True, compute='_compute_total')
    leaves = fields.Integer(string='Leaves')

    @api.onchange('type')
    def onchange_type(self):
        text = 'Test'
        dom = 'test'
        if self.type == 'trainee':
            text = "Hey Welcome Trainee"
            dom = 'IT'
        elif self.type == 'probation':
            text = "Hey Welcome Probation"
            dom = 'Management'
        return {'value': {'notes': text}, 'domain': {'department_id': [('name', '=', dom)]}}

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age <= 10 and record.gender == 'male':
                raise Exception("Hey Kiddo Grow up...")
        return True

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        print("Search Method:", args)
        return super(employee, self).search(args=args, offset=offset, limit=limit, order=order, count=count)


class department(models.Model):
    _name = "department.employee"

    _rec_name = "name"

    code = fields.Char("Code")
    name = fields.Char("Name")


class referance_detail(models.Model):
    _name = 'reference.detail'

    employee_id = fields.Many2one("employee", "Employee")

    name = fields.Char("Name")
    contact = fields.Char("Contact Number")
    email = fields.Char("Email")


class emp_hobbies(models.Model):
    _name = 'hobbies.detail'

    name = fields.Char(string='Name')
    color = fields.Integer('Color Index', default=0)


class respartner(models.Model):
    _inherit = 'res.partner'

    passport_no = fields.Char(string="Passport info")

    @api.model
    def create(self, vals):
        vals.update({'email': 'abcdef@gmail.com'})
        return super(respartner, self).create(vals)

    @api.multi
    def write(self, vals):
        vals.update({'mobile': '8306576588'})
        result = super(respartner, self).write(vals)
        print("Write method Returns:", result, type(result))
        return result

    def unlink(self):
        for rec in self:
            if rec.phone:
                raise except_orm('Warning Message', 'It is available to deactivate the record rather than deleting it.')
        return super(respartner, self).unlink()

    @api.multi
    def read(self, fields, load='_classic_read'):
        print(fields)
        res = super(respartner, self).read(fields, load=load)
        print("Read Method Returns: ", res)
        return res

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        print("Search Method", args, limit, order)
        return super(respartner, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    def copy(self, default=None):
        copy_emp = super(respartner, self).copy(default)
        print("Copy Method Returns: ", copy_emp)
        return copy_emp


class leaves(models.Model):
    _name = "leaves"
    _description = "Leaves Details"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    duration = fields.Integer(string="Duration")
    status = fields.Char(string="Status")
