from odoo import models, fields


class EstatePropertyInvoice(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one(
        "account.move", string="Invoice", readonly=True, copy=False
    )

    def set_sold(self):
        print("\n\nHello World\n\n")
        AccountMove = self.env["account.move"]
        AccountMoveLine = self.env["account.move.line"]
        for property in self:
            # Create an empty invoice
            invoice = AccountMove.create(
                {
                    "move_type": "out_invoice",  # Set the invoice type as "Customer Invoice"
                    "partner_id": property.buyer_id.id,  # Set the customer/partner for the invoice
                    "invoice_date": fields.Date.today(),  # Set the invoice date
                    # Add other required fields here
                }
            )
            # Calculate invoice lines
            selling_price = property.selling_price
            commission = selling_price * 0.06
            administrative_fees = 100.00

            # Create the first invoice line
            line1 = AccountMoveLine.create(
                {
                    "name": "Commission",  # Name of the invoice line
                    "quantity": 1,  # Quantity of the item
                    "price_unit": commission,  # Unit price
                    "move_id": invoice.id,  # Assign the invoice to the line
                }
            )

            # Create the second invoice line
            line2 = AccountMoveLine.create(
                {
                    "name": "Administrative Fees",  # Name of the invoice line
                    "quantity": 1,  # Quantity of the item
                    "price_unit": administrative_fees,  # Unit price
                    "move_id": invoice.id,  # Assign the invoice to the line
                }
            )

            # Set the invoice lines on the invoice
            invoice.write({"invoice_line_ids": [(4, line1.id), (4, line2.id)]})

            # Set the created invoice on the property
            property.invoice_id = invoice.id
        return super(EstatePropertyInvoice, self).set_sold()
