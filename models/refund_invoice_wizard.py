import time

from openerp import models, fields, api, _
from openerp.tools.safe_eval import safe_eval as eval

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    refunded = fields.Boolean(string='Refunded')


#    @api.multi
 #   @api.returns('self')
 #   def refund(self, date=None, period_id=None, description=None, journal_id=None):
  #      new_invoices = self.browse()
   #     for invoice in self:
    #        # create the new invoice
     #       values = self._prepare_refund(invoice, date=date, period_id=period_id,
      #                              description=description, journal_id=journal_id)
#	    refund_invoice = self.create(values)
 #           new_invoices += refund_invoice
#	    if invoice.sale_order:
 #               self._cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', \
  #                  (invoice.sale_order.id, refund_invoice.id))
#
 #       return new_invoices


    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
	print 'Invoice', invoice
	vals = super(AccountInvoice, self)._prepare_refund(invoice, date=date, period_id=None, \
		description=description, journal_id=journal_id)

	if invoice.sale_order:
	    vals['sale_order'] = invoice.sale_order.id
	    invoice.refunded = True

	return vals


    def action_view_refund(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #compute the number of invoices to display
        inv_ids = []
        for so in self.browse(cr, uid, ids, context=context):
	    for invoice in so.view_invoices:
		if invoice.type == 'out_refund':
		    inv_ids.append(invoice.id)

#            inv_ids += [invoice.id if invoice.type == 'out_refund' for invoice in so.invoice_ids]
        #choose the view_mode accordingly
        if len(inv_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result
