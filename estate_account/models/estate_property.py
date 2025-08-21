from odoo import fields, models

class EstateProperty(models.Model):
    
    _inherit = "estate.property"

#Override the original sold button
    def _sold_button(self):
        print("Testing that the sold action is working")
        return super().sold_button()