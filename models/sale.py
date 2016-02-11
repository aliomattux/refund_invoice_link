from openerp.osv import osv, fields


class SaleOrder(osv.osv):
    _inherit = 'sale.order'
    _columns = {
	'view_invoices': fields.one2many('account.invoice', 'sale_order', 'Invoices'),
    }


    def action_view_refund(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one inv$
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
