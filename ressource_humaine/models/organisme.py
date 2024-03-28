# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHOrganisme(models.Model):
    _name = 'rh.organisme'
    _rec_name = 'rs_organisme'

    code_organisme = fields.Char()
    rs_organisme = fields.Char()
    adresse_organisme = fields.Char()
    organisme_file_lines = fields.One2many('rh.file', 'organisme_id')




