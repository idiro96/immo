from odoo import models, fields, api, _


class OrganizationChart(models.TransientModel):
    _name = 'organization.chart'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_organization_chart').report_action(self)


class OrganizationChartReport(models.AbstractModel):
    _name = 'report.ressource_humaine.organization_chart_report'

    @api.model
    def get_report_values(self, docids, data=None):
        ressource_humaine = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الموارد البشرية'),
                                                            ('fin_relation', '=', False)])
        budget_comptabilite = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الميزانية'),
                                                              ('fin_relation', '=', False)])
        informatique = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الإعلام'),
                                                       ('fin_relation', '=', False)])
        mgx = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الوسائل العامة'),
                                              ('fin_relation', '=', False)])
        internat = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'النظام الداخلي'),
                                                   ('fin_relation', '=', False)])
        etude_1 = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', '%مديرية الدراسات%'),
                                                  ('fin_relation', '=', False)])
        print(etude_1)
        etude_2 = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', '%مديرية الدرسات%'),
                                                  ('fin_relation', '=', False)])
        print(etude_2)
        etude = etude_1 + etude_2
        print(etude)
        stage = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التربصات'),
                                                ('fin_relation', '=', False)])
        formation = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التكوين'),
                                                    ('fin_relation', '=', False)])
        recherche = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'البحث'),
                                                    ('fin_relation', '=', False)])

        report_data = {
            'company': self.env.user.company_id,
            'ressource_humaine': ressource_humaine,
            'budget_comptabilite': budget_comptabilite,
            'informatique': informatique,
            'mgx': mgx,
            'internat': internat,
            'etude': etude,
            'stage': stage,
            'formation': formation,
            'recherche': recherche,
        }

        return report_data
