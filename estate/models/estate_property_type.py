from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string="Name", required=True)

    # One property type can be applied to many properties
    property_ids = fields.One2many("estate.property", "property_type_id")
