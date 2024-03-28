# -*- coding: utf-8 -*-
from odoo import http

# class RessourceHumaine(http.Controller):
#     @http.route('/ressource_humaine/ressource_humaine/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ressource_humaine/ressource_humaine/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ressource_humaine.listing', {
#             'root': '/ressource_humaine/ressource_humaine',
#             'objects': http.request.env['ressource_humaine.ressource_humaine'].search([]),
#         })

#     @http.route('/ressource_humaine/ressource_humaine/objects/<model("ressource_humaine.ressource_humaine"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ressource_humaine.object', {
#             'object': obj
#         })