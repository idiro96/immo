# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHPromotionLine(models.Model):
    _name = 'rh.promotion.line'

    date_examin_professionnel = fields.Date()
    date_promotion = fields.Date()
    promotion_id = fields.Many2one('rh.promotion')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    job_id = fields.Many2one('hr.job')
    grade_old_id = fields.Many2one('rh.grade')
    grade_id = fields.Many2one('rh.grade')
    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    date_grade = fields.Date()
    type_fonction_id = fields.Many2one('rh.type.fonction')
    promotion_line_file_line = fields.Binary()
    duree = fields.Integer()
    imprimer = fields.Boolean(Default=False)
    code_line = fields.Char()
    date_creation = fields.Char(compute="_compute_date", store=True)
    ref_promotion = fields.Char()
    date_ref_promotion = fields.Date()
    ancien_index = fields.Integer()

    @api.depends('code_line')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                # Convertit le champ en un objet datetime
                datetime_object = record.create_date.split(' ')
                # Récupère uniquement la date
                date_creation = datetime_object[0]
                record.date_creation = date_creation



