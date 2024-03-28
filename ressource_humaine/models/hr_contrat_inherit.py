# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class HrContratInherited(models.Model):
    _inherit = 'hr.contract'

    name = fields.Char('Contract Reference', required=True, readonly=True, default=lambda self: _('New'))
    corps_id = fields.Many2one('rh.corps', readonly=True, compute='_compute_employee_fields')
    grade_id = fields.Many2one('rh.grade', readonly=True, compute='_compute_employee_fields')
    groupe_id = fields.Many2one('rh.groupe', readonly=False)
    department_id = fields.Many2one('hr.department', readonly=True, related='employee_id.department_id',
                                    compute='_compute_employee_fields', store=True)
    job_id = fields.Many2one('hr.job', readonly=True, compute='_compute_employee_fields')
    type = fields.Selection([('contrat', 'Contrat'), ('decision', 'Decision'), ]
                            , required=True, default='contrat')

    date_start = fields.Date('Start Date', readonly=True, help="Start date of the contract.")
    point_indiciare = fields.Integer()
    indice_minimal = fields.Integer()
    indice_base = fields.Integer()
    bonification_indiciaire = fields.Integer()
    categorie_id = fields.Many2one('rh.categorie')
    categorie_superieure_id = fields.Many2one('rh.categorie.superieure')
    echelon_id = fields.Many2one('rh.echelon')
    niveau_hierarchique_id = fields.Many2one('rh.niveau.hierarchique')
    section_id = fields.Many2one('rh.section')
    section_superieure_id = fields.Many2one('rh.section.superieure')
    grille_id = fields.Many2one('rh.grille')
    bool1 = fields.Boolean(default=True)
    code_type_fonction = fields.Char(related='employee_id.nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)

    wage_range = fields.Selection([
        ('low', '15000-30000'),
        ('medium', '30000-50000'),
        ('high', '50000-100000'),
        ('very_high', '100000+')
    ], compute='_compute_wage_range', store=True)

    @api.depends('wage')
    def _compute_wage_range(self):
        for rec in self:
            if rec.wage < 30000:
                rec.wage_range = 'low'
            elif 30000 <= rec.wage < 50000:
                rec.wage_range = 'medium'
            elif 50000 <= rec.wage < 100000:
                rec.wage_range = 'high'
            else:
                rec.wage_range = 'very_high'

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.contract.inhert') or _('New')

        result = super(HrContratInherited, self).create(vals)
        employee = self.env['hr.employee'].search(
            [('id', '=', result.employee_id.id)])
        if employee.nature_travail_id.code_type_fonction == 'fonction':
            employee.write({
                'date_avancement': result.date_start,
            })
            employee.write({
                'groupe_id': result.groupe_id.id,
            })
            employee.write({
                'categorie_id': result.categorie_id.id,
            })
            employee.write({
                'echelon_id': result.echelon_id.id,
            })
            employee.write({
                'ref': result.name,
            })
            employee.write({
                'date_ref': result.date_start,
            })
            result.employee_id.point_indiciare = result.echelon_id.indice_echelon
            result.employee_id.wage = result.indice_minimal * 45 + result.point_indiciare * 45
            employee.write({
                'wage': result.employee_id.wage,
            })
        elif employee.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
            employee.write({
                'date_avancement': result.date_start,
            })
            employee.write({
                'section_id': result.section_id.id,
            })
            employee.write({
                'categorie_id': result.categorie_id.id,
            })
            employee.write({
                'echelon_id': result.echelon_id.id,
            })
            employee.write({
                'ref': result.name,
            })
            employee.write({
                'date_ref': result.date_start,
            })
            result.employee_id.point_indiciare = result.echelon_id.indice_echelon
            result.employee_id.wage = result.indice_base * 45 + result.point_indiciare
            employee.write({
                'wage': result.employee_id.wage,
            })

        return result

    @api.constrains('date_start', 'date_end', 'employee_id')
    def _check_contract_overlap(self):
        for contract in self:
            if not contract.date_end:  # If there's no end date
                # Check if the employee has any other contracts with no end date
                same_employee_contracts = self.search([
                    ('employee_id', '=', contract.employee_id.id),
                    ('date_end', '=', False),
                    ('id', '!=', contract.id),
                ])
                if same_employee_contracts:
                    raise ValidationError("This employee already has a contract with no end date.")
            else:
                overlapping_contracts = self.search([
                    ('employee_id', '=', contract.employee_id.id),
                    ('date_start', '<=', contract.date_end),
                    ('date_end', '>=', contract.date_start),
                    ('id', '!=', contract.id),
                ])
                if overlapping_contracts:
                    raise ValidationError("This employee has a contract within this period.")

    @api.depends('trial_date_end')
    def _compute_months_passed(self):
        for contract in self:
            if contract.trial_date_end:
                enter_date = fields.Date.from_string(contract.date_start)
                end_date = fields.Date.from_string(contract.trial_date_end)
                months_passed = (end_date.year - enter_date.year) * 12 + end_date.month - enter_date.month
                contract.months_passed = months_passed
            else:
                contract.months_passed = 0

    months_passed = fields.Integer(compute='_compute_months_passed', string='Months Passed During Trial Period',
                                   store=True)

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_hr_contract_report').report_action(self)

    @api.multi
    def print_pv(self):
        return self.env.ref('ressource_humaine.report_pv_instalation').report_action(self)

    @api.multi
    def print_renew(self):
        return self.env.ref('ressource_humaine.action_renew_contract_report').report_action(self)

    @api.onchange('type')
    def onchange_type(self):
        for rec in self:
            domain = []
            if rec.type == 'contrat':
                print('hkf')
                rec.bool1 = False
                # type_fonction = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'contractuel')])
                # job = self.env['hr.job'].search([('nature_travail_id', '=', type_fonction.id)])
                # employee = self.env['hr.employee'].search([('job_id', '=', job.id)])
                employee = self.env['hr.employee'].search([('nature_travail_id.code_type_fonction', '=', 'contractuel'),
                                                           ('fin_relation', '=', False),])

                print(employee)
                domain.append(('id', 'in', employee.ids))
            else:
                type_fonction = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'contractuel')])
                if type_fonction.code_type_fonction == 'fonctionsuperieure':
                    rec.bool1 = False
                else:
                    rec.bool1 = True
                # job = self.env['hr.job'].search([('nature_travail_id', '=', type_fonction.id)])
                employee = self.env['hr.employee'].search([('nature_travail_id', '!=', type_fonction.id)])
                domain.append(('id', 'in', employee.ids))
        res = {'domain': {'employee_id': domain}}

        return res

    @api.onchange('groupe_id')
    def onchange_groupe(self):
        for rec in self:
            domain = []
            if rec.groupe_id:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', rec.groupe_id.id)])
                print(categorie)
                domain.append(('id', 'in', categorie.ids))
            else:
                categorie = self.env['rh.categorie'].search([('groupe_id', '=', None)])
                print(categorie)
                domain.append(('id', 'in', categorie.ids))

        res = {'domain': {'categorie_id': domain}}
        print(res)
        return res

    @api.onchange('categorie_id')
    def onchange_categorie(self):
        for rec in self:
            domain = []
            if rec.categorie_id:
                echelon = self.env['rh.echelon'].search([('categorie_id', '=', rec.categorie_id.id)])
                section = self.env['rh.section'].search([('categorie_id', '=', rec.categorie_id.id)])
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'contractuel':
                    rec.indice_minimal = rec.categorie_id.Indice_minimal
                    rec.wage = rec.indice_minimal * 45
                elif type_fonction.code_type_fonction == 'fonction':
                    print('beny')
                    domain.append(('id', 'in', echelon.ids))
                    rec.indice_minimal = rec.categorie_id.Indice_minimal

                elif type_fonction.code_type_fonction == 'postesuperieure':
                    domain.append(('id', 'in', echelon.ids))
                    rec.indice_minimal = rec.categorie_id.Indice_minimal
                else:
                    domain.append(('id', 'in', section.ids))

            res = {'domain': {'echelon_id': domain}}

        return res

    @api.onchange('section_id')
    def onchange_section(self):
        domain = []
        for rec in self:
            if rec.section_id:
                rec.indice_base = rec.section_id.indice_base
                echelon = self.env['rh.echelon'].search([('section', '=', rec.section_id.id)])
                domain.append(('id', 'in', echelon.ids))
                rec.indice_minimal = rec.categorie_id.Indice_minimal
            res = {'domain': {'echelon_id': domain}}
        return res

    @api.onchange('niveau_hierarchique_id')
    def onchange_niveau_hierarchique(self):
        for rec in self:
            if rec.niveau_hierarchique_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'postesuperieure':
                    rec.bonification_indiciaire = rec.niveau_hierarchique_id.bonification_indiciaire
                    rec.wage = (rec.indice_minimal * 45 + rec.point_indiciare * 45) + rec.bonification_indiciaire

    @api.onchange('echelon_id')
    def onchange_echelon(self):
        for rec in self:
            domain = []
            if rec.echelon_id:
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'postesuperieure':
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                elif type_fonction.code_type_fonction == 'fonction':
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                    rec.wage = rec.indice_minimal * 45 + rec.point_indiciare * 45
                else:
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                    rec.wage = rec.indice_base * 45 + rec.point_indiciare

    @api.onchange('employee_id')
    def onchange_employee(self):
        for rec in self:
            domain = []
            if rec.employee_id:
                for rec in self:
                    self.date_start = self.employee_id.date_entrer
                type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.employee_id.nature_travail_id.id)])
                if type_fonction.code_type_fonction == 'contractuel':
                    categorie = self.env['rh.categorie'].search([('type_fonction_id', '=', type_fonction.id)])
                    domain.append(('id', 'in', categorie.ids))
                elif type_fonction.code_type_fonction == 'fonctionsuperieure':
                    categorie = self.env['rh.categorie'].search([('type_fonction_id', '=', type_fonction.id)])
                    domain.append(('id', 'in', categorie.ids))
                    rec.point_indiciare = rec.echelon_id.indice_echelon
                elif type_fonction.code_type_fonction == 'fonction':
                    domain = None
                else:
                    domain = None

        res = {'domain': {'categorie_id': domain}}
        return res

    @api.depends('employee_id')
    def _compute_employee_fields(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id.id if rec.employee_id else False
            rec.job_id = rec.employee_id.job_id.id if rec.employee_id else False
            rec.corps_id = rec.employee_id.corps_id.id if rec.employee_id else False
            rec.grade_id = rec.employee_id.grade_id.id if rec.employee_id else False

    @api.onchange('employee_id')
    def onchange_employee_type_id(self):
        if self.employee_id:
            self.type_id = self.employee_id.type_id


class HrContractReport(models.AbstractModel):
    _name = 'report.ressource_humaine.hr_contract_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employees = self.env['hr.employee'].browse(docids)

        employee_date_entrer = {}
        for employee in employees:
            date_entrer = employee.date_entrer
            formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%d/%m/%Y")
            employee_date_entrer[employee.id] = formatted_date_entrer

        employee_date_fin_relation = {}
        for employee in employees:
            date_fin_relation = employee.date_fin_relation
            if date_fin_relation:
                formatted_date_fin_relation = datetime.strptime(date_fin_relation, "%Y-%m-%d").strftime("%d/%m/%Y")
                employee_date_fin_relation[employee.id] = formatted_date_fin_relation
            else:
                employee_date_fin_relation[employee.id] = ''
        print(employee_date_fin_relation)

        employee_birthday = {}
        for employee in employees:
            birthday = employee.birthday
            if birthday:
                formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%d-%m-%Y")
                employee_birthday[employee.id] = formatted_birthday
            else:
                employee_birthday[employee.id] = ''

        report_data = {
            'employee_birthday': employee_birthday,
            'employee_date_fin_relation': employee_date_fin_relation,
            'employee_date_entrer': employee_date_entrer,
            'employees': employees,
            'company': self.env.user.company_id,
        }

        return report_data
