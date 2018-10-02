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


{
    'name': 'Account Partner Payment',
    'version': '0.1',
    'category': 'Banking addons',
    'license': 'AGPL-3',
    'summary': 'Adds payment type and receivable bank account on partners',
    'description': """
Account Partner Payment
=======================

This module adds severals fields :

* the *Supplier Payment Type* and *Customer Payment Type* on Partners,

* the *Receivable Bank Account* on Partners,

* the *Payment Type* on Invoices.

On a Payment Order, in the wizard *Select Invoices to Pay*, the invoices will
be filtered per Payment Type.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com>
for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_banking_payment_export'],
    'data': [
        'view/partner.xml',
        'view/account_invoice.xml',
    ],
    'demo': [],
    'active': False,
}
