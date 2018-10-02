# -*- coding: utf-8 -*-
# © 2013-2014 ACSONE SA (<http://acsone.eu>).
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_order_ok = fields.Boolean(
        related='payment_mode_id.payment_order_ok', readonly=True)

    @api.model
    def _get_reference_type(self):
        rt = super(AccountInvoice, self)._get_reference_type()
        rt.append(('structured', _('Structured Reference')))
        return rt

    @api.model
    def line_get_convert(self, line, part):
        """Copy supplier bank account from invoice to account move line"""
        res = super(AccountInvoice, self).line_get_convert(line, part)
        if line.get('type') == 'dest' and line.get('invoice_id'):
            invoice = self.browse(line['invoice_id'])
            if invoice.type in ('in_invoice', 'in_refund'):
                res['partner_bank_id'] = invoice.partner_bank_id.id or False
        return res

    @api.multi
    def _prepare_new_payment_order(self):
        self.ensure_one()
        vals = {
            'payment_mode_id': self.payment_mode_id.id,
            'payment_type': self.payment_mode_id.payment_type,
            }
        if self.payment_mode_id.bank_account_link == 'fixed':
            vals['journal_id'] = self.payment_mode_id.fixed_journal_id.id
        # TODO : else: no filter on allowed bank accounts, because onchange not played ??
        return vals

    @api.multi
    def create_account_payment_line(self):
        apoo = self.env['account.payment.order']
        aplo = self.env['account.payment.line']
        action = {}
        for inv in self:
            if not inv.payment_mode_id:
                raise UserError(_(
                    "No Payment Mode on invoice %s") % inv.number)
            if not inv.move_id:
                raise UserError(_(
                    "No Journal Entry on invoice %s") % inv.number)
            payorders = apoo.search([
                ('payment_mode_id', '=', inv.payment_mode_id.id),
                ('state', '=', 'draft')])
            if payorders:
                payorder = payorders[0]
                new_payorder = False
            else:
                payorder = apoo.create(inv._prepare_new_payment_order())
                new_payorder = True
            count = 0
            for line in inv.move_id.line_ids:
                if line.account_id == inv.account_id and not line.reconciled:
                    paylines = aplo.search([
                        ('move_line_id', '=', line.id),
                        ('state', '!=', 'cancel')])
                    if paylines:
                        continue
                    line.create_payment_line_from_move_line(payorder)
                    count += 1
            if count:
                if new_payorder:
                    inv.message_post(_(
                        '%d payment lines added to the new draft payment '
                        'order %s which has been automatically created.')
                        % (count, payorder.name))
                else:
                    inv.message_post(_(
                        '%d payment lines added to the existing draft '
                        'payment order %s.')
                        % (count, payorder.name))
            else:
                raise UserError(_(
                    'No Payment Line created for invoice %s because '
                    'it already exists or because this invoice is '
                    'already paid.') % inv.number)
            action = self.env['ir.actions.act_window'].for_xml_id(
                'account_payment_order',
                'account_payment_order_%s_action' % payorder.payment_type)
            action.update({
                'view_mode': 'form,tree,pivot,graph',
                'res_id': payorder.id,
                'views': False,
                })
        return action
