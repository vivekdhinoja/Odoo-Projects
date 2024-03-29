# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import api, fields, models, _,tools


class ProjectPhase(models.Model):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'sequence'
    
    name = fields.Char(string='Phase Name')
    sequence = fields.Integer(string='Sequence')
    project_id = fields.Many2one('project.project',string='Project',default=lambda self: self.env.context.get('default_project_id'))
    start_date = fields.Date(string='Start Date', copy=False)
    end_date = fields.Date(string='End Date', copy=False)
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env['res.company']._company_default_get())
    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.uid)
    task_count = fields.Integer(compute="get_task",string='Count')
    notes = fields.Text(string='Notes')
    task_alloc = fields.One2many('task.allocation', "task_allocation_id", 'Task / Resource Allocation')

    @api.multi
    def action_project_phase_task(self):
        self.ensure_one()
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('phase_id', '=', self.id)],
        }
    
    @api.multi
    def get_task(self):
        for rec in self:
            records = self.env['project.task'].search([('phase_id','=',rec.id)])
            rec.task_count = len(records)


class Task(models.Model):
    _inherit = 'project.task'    
    
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')


class taskAlloc(models.Model):
    _name = "task.allocation"

    task_allocation_id = fields.Many2one('project.task.phase', string='Task Allocation')
    user_id = fields.Many2one('res.users',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always', string='Resources')
    task_id = fields.Char(string='Task')

    @api.multi
    def create_task(self):
        print("Hello from Create Task Button Method")
        vals = {'user_id': self.user_id.id, 'name': self.task_id}
        return self.env['project.task'].create(vals)

    def view_task(self):
        print("Hello from View Task Button Method")
        view = self.env.ref('project.view_task_form2')
        # my_action_id =
        # my_menu_id =
        res_id = self.env['project.task'].search([('user_id', '=', self.user_id.id ), ('name', '=', self.task_id)], )
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        # view_id_str = str(view.id)
        my_action_id_str = str(self.env.ref('project.action_view_task').id)
        my_menu_id_str = str(self.env.ref('project.menu_action_view_task').id)
        # print("My View Id String: ", view_id_str, my_action_id_str, my_menu_id_str, res_id)
        my_new_task_url = base_url + "/web?&debug=#id=" + str(res_id.id) + "&view_type=form&model=project.task&menu_id=" + my_menu_id_str + "&action=" + my_action_id_str

        return {
            'name': ('View Task'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'project.task',
            # 'type': 'ir.actions.act_window',
            'res_id': res_id.id,
            'url': my_new_task_url,
            'type': 'ir.actions.act_url',
            # 'target':'new',
        }

    
class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    project_phase_count = fields.Integer('Job Note', compute='_get_project_phase_count')
    
    @api.multi
    def _get_project_phase_count(self):
        for project_phase in self:
            project_phase_ids = self.env['project.task.phase'].search([('project_id','=',project_phase.id)])
            project_phase.project_phase_count = len(project_phase_ids)
        
    @api.multi
    def action_project_phase(self):
        self.ensure_one()
        return {
            'name': 'Phases',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task.phase',
            'domain': [('project_id', '=', self.id)],
        }
        
class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"
    
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')
    
    
    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                    t.date_start as date_start,
                    t.date_end as date_end,
                    t.date_last_stage_update as date_last_stage_update,
                    t.date_deadline as date_deadline,
                    t.user_id,
                    t.phase_id,
                    t.project_id,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id as stage_id,
                    t.kanban_state as state,
                    t.working_days_close as working_days_close,
                    t.working_days_open  as working_days_open,
                    (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,
                    create_date,
                    write_date,
                    date_start,
                    date_end,
                    date_deadline,
                    date_last_stage_update,
                    t.user_id,
                    t.phase_id,
                    t.project_id,
                    t.priority,
                    name,
                    t.company_id,
                    t.partner_id,
                    stage_id
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM project_task t
                WHERE t.active = 'true'
                %s
        """ % (self._table, self._select(), self._group_by()))
    


