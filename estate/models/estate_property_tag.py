from odoo import fields, models

class EstatePropertyTaf(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(string='Name', required=True)

    color = fields.Integer('Color')
