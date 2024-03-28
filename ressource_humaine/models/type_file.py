from odoo import models, fields, api, _


class RHTypeFile(models.Model):
    _name = 'rh.type.file'
    _rec_name = 'intitule'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule = fields.Char()
    intitule_fr = fields.Char()
    type_file = fields.Selection(
        [('indisponibilite', 'Indisponibilite'), ('sanction', 'Sanction'), ('formation', 'Formation'),
         ('finrelation', 'Fin Relation'), ('accidenttravail', 'Accident Travail'), ('controlemedicale', 'Contrôle Médicale'),
         ('employe', 'Employe'), ('promotion', 'Promotion'), ('avancement', 'Avancement'), ('autre', 'Autres')], default = 'draft')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.file.sequence') or _('New')
        result = super(RHTypeFile, self).create(vals)
        return result



