from odoo import fields, models, _
from odoo.fields import Command

class EstateProperty(models.Model):
    
    _inherit = "estate.property"

#Override the original sold button
    def _sold_button(self):
        res = super().sold_button()

        for record in self:
            if not record.buyer_id:
                raise UserError(_("Cannot generate invoice without a buyer"))
            
            self.env['account.move'].create({
            'partner_id': record.buyer_id.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': record.name,
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06
                }),
                Command.create({
                    'name': "Admin Fees",
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
            })

        return res