# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Partner Payment module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm


class payment_order_create(orm.TransientModel):
    _inherit = 'payment.order.create'

    def extend_payment_order_domain(
            self, cr, uid, payment_order, domain, context=None):
        super(payment_order_create, self).extend_payment_order_domain(
            cr, uid, payment_order, domain, context=context)
        domain += [
            '|', '|',
            ('invoice', '=', False),
            ('invoice.payment_mode_type', '=', False),
            ('invoice.payment_mode_type', '=', payment_order.mode_type.id)
            ]
        return True
