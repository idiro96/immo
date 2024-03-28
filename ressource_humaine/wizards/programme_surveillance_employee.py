from odoo import models, fields, api, _



class ProgrammeEmployee(models.TransientModel):

    _name = 'programme.employee'
    employee_id = fields.Many2one('hr.employee',  string="nom de l'employee")
    numero= fields.Integer(string="numero")

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_notice_planning_surveillance').report_action(self)
