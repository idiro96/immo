from odoo import models, fields, api, _


class ArretSalaire(models.TransientModel):

    _name = 'arret.salaire'

    employee_id = fields.Many2one('hr.employee', required='True')
    numero_decision_arret= fields.Integer(required='True')
    date_arret_salaire=fields.Date(required='True')

    numero_decision_titularisation = fields.Integer()
    date_decision_titularisation= fields.Date()
    date_titularisation= fields.Date()

    motif = fields.Selection([('نهاية علاقة العمل','نهاية علاقة العمل '),('الاحالة على التقاعد','الاحالة على التقاعد'),( 'عطلة مرضية طويلة المدى', 'عطلة مرضية طويلة المدى' ), ('الاحالة على الاستيداع لاغراض شخصية','الاحالة على الاستيداع لاغراض شخصية ')], required='True')
    date_motif = fields.Date(required='True')

    def print_report(self):
        return self.env.ref('ressource_humaine.action_arret_retraite').report_action(self)
