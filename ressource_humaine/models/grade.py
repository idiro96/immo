# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from werkzeug.routing import ValidationError


class RHGrade(models.Model):
    _name = 'rh.grade'
    _rec_name = 'intitule_grade'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_grade = fields.Char(required=True)
    intitule_grade_fr = fields.Char('Intitulé Grade', required=True)
    corps_id = fields.Many2one(comodel_name='rh.corps')
    filiere_id = fields.Many2one(comodel_name='rh.filiere')
    loi_id = fields.Many2one(comodel_name='rh.loi')
    grade_id = fields.Many2one('hr.groupe')
    categorie_id = fields.Many2one('rh.categorie')
    employee_ids = fields.One2many('hr.employee', 'grade_id', string='Employees', groups='base.group_user')
    no_of_employee_cdi_plein = fields.Integer(compute='_compute_employees_contract', store=True)
    no_of_employee_cdd_plein = fields.Integer(compute='_compute_employees_contract', store=True)
    no_of_employee_cdi_partiel = fields.Integer(compute='_compute_employees_contract', store=True)
    no_of_employee_cdd_partiel = fields.Integer(compute='_compute_employees_contract', store=True)
    no_of_employee = fields.Integer(compute='_compute_employees', store=True)
    max_employee = fields.Integer(default=10, store=True)
    nombre_de_postes_vacants = fields.Integer(compute='_compute_nombre_de_postes_vacants', store=True)

    @api.depends('employee_ids.grade_id', 'employee_ids.active')
    def _compute_employees(self):
        employee_data = self.env['hr.employee'].read_group([('grade_id', 'in', self.ids)], ['grade_id'], ['grade_id'])
        result = dict((data['grade_id'][0], data['grade_id_count']) for data in employee_data)
        for grade in self:
            grade.no_of_employee = result.get(grade.id, 0)

    @api.depends('employee_ids.grade_id', 'employee_ids.active', 'employee_ids.type_id.code_type_contract')
    def _compute_employees_contract(self):
        contract_types = {
            'pleintemps_indeterminee': 'no_of_employee_cdi_plein',
            'pleintemps_determinee': 'no_of_employee_cdd_plein',
            'partiel_indeterminee': 'no_of_employee_cdi_partiel',
            'partiel_determinee': 'no_of_employee_cdd_partiel',
        }

        for contract_type, field_name in contract_types.items():
            employee_data = self.env['hr.employee'].read_group(
                [
                    ('grade_id', 'in', self.ids),
                    ('type_id.code_type_contract', '=', contract_type)
                ],
                ['grade_id'], ['grade_id']
            )
            result = dict((data['grade_id'][0], data['grade_id_count']) for data in employee_data)
            for grade in self:
                setattr(grade, field_name, result.get(grade.id, 0))

    # @api.constrains('no_of_employee', 'max_employee')
    # def _check_max_employee_limit(self):
    #     for job in self:
    #         if job.no_of_employee > job.max_employee:
    #             raise ValidationError("لا يجوز أن عدد الموظفين يتفوق عن الحد الأقصى المسموح به")

    @api.depends('max_employee', 'no_of_employee')
    def _compute_nombre_de_postes_vacants(self):
        for job in self:
            job.nombre_de_postes_vacants = job.max_employee - job.no_of_employee

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.grade.sequence') or _('New')
        result = super(RHGrade, self).create(vals)
        return result

    @api.onchange('loi_id')
    def onchange_loi_id(self):
        if self.loi_id:
            filiere_domain = [('loi_id', '=', self.loi_id.id)]
            corps_domain = [('loi_id', '=', self.loi_id.id)]
            if self.filiere_id:
                filiere_domain.append(('id', '=', self.filiere_id.id))
                corps_domain.append(('filiere_id', '=', self.filiere_id.id))
            return {'domain': {'filiere_id': filiere_domain, 'corps_id': corps_domain}}
        else:
            return {'domain': {'filiere_id': [], 'corps_id': []}}

    @api.onchange('filiere_id')
    def onchange_filiere_id(self):
        if self.filiere_id:
            return {'domain': {'corps_id': [('filiere_id', '=', self.filiere_id.id)]}}
        else:
            return {'domain': {'corps_id': []}}

    # @api.onchange('loi_id')
    # def _onchange_related_field_loi(self):
    #     # This method will be called when the value of 'related_field' changes
    #     # Update the domain for 'field1' based on the value of 'related_field'
    #     print('teste')
    #     for rec in self:
    #         domain = []
    #         if rec.loi_id:
    #             print('teste')
    #             filiere = self.env['rh.filiere'].search([('loi_id', '=', rec.loi_id.id)])
    #             print(filiere)
    #             domain.append(('id', 'in', filiere.ids))
    #         else:
    #             domain = ''
    #
    #     res = {'domain': {'filiere_id': domain}}
    #     print(res)
    #     return res
    #
    # @api.onchange('filiere_id')
    # def _onchange_related_field_filier(self):
    #     print('teste')
    #     for rec in self:
    #         domain = []
    #         if rec.filiere_id:
    #             print('teste')
    #             corps = self.env['rh.corps'].search([('filiere_id', '=', rec.filiere_id.id)])
    #             print(corps)
    #             if not rec.filiere_id:
    #                 corps = self.env['rh.corps'].search([('loi_id', '=', rec.loi_id.id)])
    #                 domain.append(('id', 'in', corps.ids))
    #         else:
    #             domain = ''
    #
    #     res = {'domain': {'corps_id': domain}}
    #     print(res)
    #     return res