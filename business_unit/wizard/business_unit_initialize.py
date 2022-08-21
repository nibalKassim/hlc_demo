from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessUnitInitialize(models.TransientModel):
    
    _name = 'business.unit.initialize'
    _description = 'Business Unit Initialization Wizard'
    
    @api.model
    def default_get(self,default_fields):
        res = super(BusinessUnitInitialize, self).default_get(default_fields)
        aid = self.env.context.get('active_id', False)
        if aid:
            bu = self.env['business.unit'].browse(aid)
            res['code_sale_seq'] = bu.sale_sequence_id.prefix if bu.sale_sequence_id else f'SO/{bu.code}/%(range_year)s/'
            res['name_sale_team'] =  f'Sales- {bu.name}'
            res['name_jrnl_sale'] = f'Customer Invoices - {bu.name}'
            res['code_jrnl_sale'] = f'INV-{bu.code}'[:5]
            res['seq_jrnl_sale'] = f'INV/{bu.code}/%(range_year)s/'
            res['seq_rfnd_sale'] = f'RINV/{bu.code}/%(range_year)s/'
            res['name_jrnl_purchase'] = f'Vendor Bills - {bu.name}'
            res['code_jrnl_purchase'] = f'BL-{bu.code}'[:5]
            res['seq_jrnl_purchase'] = f'BILL/{bu.code}/%(range_year)s/'
            res['seq_rfnd_purchase'] = f'RBILL/{bu.code}/%(range_year)s/'
            res['name_jrnl_cash'] = f'Cash - {bu.name}'
            res['code_jrnl_cash'] = f'CS-{bu.code}'[:5]
            res['seq_jrnl_cash'] = f'CSH/{bu.code}/%(range_year)s/'
            res['name_jrnl_bank'] = f'Bank - {bu.name}'
            res['code_jrnl_bank'] = f'BN-{bu.code}'[:5]
            res['seq_jrnl_bank'] = f'BNK/{bu.code}/%(range_year)s/'
        return res
    
    is_sale_seq = fields.Boolean(
        string='Sale Sequence',
        default=False
        )
    code_sale_seq = fields.Char(
        string='Sale Seq Code',
        )
    is_sale_team = fields.Boolean(
        string='Sale Team',
        default=False
        )
    name_sale_team = fields.Char(
        string='Sale Team Name',
        ) 

    is_new_warehouse = fields.Boolean(
        string='New Warehouse',
        default=False
        )
    name_new_warehouse = fields.Char(
        string='Warehouse Name',
        )
    is_jrnl_sale = fields.Boolean(
        string='Sale journal',
        default=False
        )
    code_jrnl_sale = fields.Char(
        string='Sale Jrnl Short Code',
        size=5,
        )
    name_jrnl_sale = fields.Char(
        string='Sale Journal Name',
        )
    seq_jrnl_sale = fields.Char(
        string='Sequence Prefix',
        )
    seq_rfnd_sale = fields.Char(
        string='Sale Refund Seq Prefix',
         )    
    
    is_jrnl_purchase = fields.Boolean(
        string='Purchase journal',
        default=False
        )
    name_jrnl_purchase = fields.Char(
        string='Purchase Journal Name',
        )
    code_jrnl_purchase = fields.Char(
        string='Purchase Jrnl Short Code',
        size=5,
        )
    seq_jrnl_purchase = fields.Char(
        string='Purchase Sequence Prefix',
        )
    seq_rfnd_purchase = fields.Char(
        string='Purchase Refund Seq Prefix',
        )    
    is_jrnl_cash = fields.Boolean(
        string='Cash journal',
        default=False
        )
    name_jrnl_cash = fields.Char(
        string='Cash Journal Name',
        )
    code_jrnl_cash = fields.Char(
        string='Cash Short Code',
        size=5,
        )
    seq_jrnl_cash = fields.Char(
        string='Cash Sequence Prefix',
        )
    is_jrnl_bank = fields.Boolean(
        string='Bank journal',
        default=False
        )
    name_jrnl_bank = fields.Char(
        string='Bank Journal Name',
        )
    code_jrnl_bank = fields.Char(
        string='Bank Short Code',
        size=5,
        )
    seq_jrnl_bank = fields.Char(
        string='Bank Sequence Prefix',
        )
    
    @api.model
    def _create_sequence(self, name, prefix, co, impl='no_gap'):
        seq_dict = {
            'name':name,
            'implementation': impl,
            'prefix': prefix,
            'padding': 4,
            'number_increment': 1,
            'use_date_range': True,
            'company_id': co,            
            }
        return self.env['ir.sequence'].create(seq_dict).id

    def initialize_bu(self):
        aid = self.env.context.get('active_id', False)
        if not aid:
            raise ValidationError(_('An error is preventing this process to continue./n Please repeat the initialization.'))
        bu = self.env['business.unit'].browse(aid)
        vals = {}
        if self.is_sale_seq:
            if bu.sale_sequence_id != self.code_sale_seq:
                name = _('Sale') + '-' + bu.name
                vals['sale_sequence_id'] = self._create_sequence(name, self.code_sale_seq, bu.company_id.id, 'standard')
        if self.is_sale_team:
            team_dict = {
                    'name': self.name_sale_team,
                    'use_quotations':False,
                    'team_type': 'sales',
                    'business_unit_id': bu.id,
                    'company_id': bu.company_id.id,            
                }
            vals['crm_team_ids'] = [(0,0,team_dict)]

        if self.is_jrnl_sale:
            jrnl_dict = {
                'name': self.name_jrnl_sale,
                'type': 'sale',
                'code': self.code_jrnl_sale,
                'sequence_id':self._create_sequence(self.code_jrnl_sale + '-' + _('Sequence'), self.seq_jrnl_sale, bu.company_id.id),
                'business_unit_id': bu.id,
                'company_id': bu.company_id.id            
                }
            if self.seq_rfnd_sale:
                jrnl_dict['refund_sequence'] = True
                jrnl_dict['refund_sequence_id'] = self._create_sequence(self.code_jrnl_sale + '-' + _('Refund Sequence'), 
                                                            self.seq_rfnd_sale, bu.company_id.id)
            else:
                jrnl_dict['refund_sequence'] = False        
            vals.setdefault('journal_ids',[]).append((0,0,jrnl_dict))     
                
        if self.is_jrnl_purchase:
            jrnl_dict = {
                'name': self.name_jrnl_purchase,
                'type': 'purchase',
                'code': self.code_jrnl_purchase,
                'sequence_id':self._create_sequence(self.code_jrnl_purchase + '-' + _('Sequence'), self.seq_jrnl_purchase, bu.company_id.id),
                'business_unit_id': bu.id,
                'company_id': bu.company_id.id            
                }
            if self.seq_rfnd_purchase:
                jrnl_dict['refund_sequence'] = True
                jrnl_dict['refund_sequence_id'] = self._create_sequence(self.code_jrnl_purchase + '-' + _('Refund Sequence'), 
                                                            self.seq_rfnd_purchase, bu.company_id.id)
            else:
                jrnl_dict['refund_sequence'] = False
            vals.setdefault('journal_ids',[]).append((0,0,jrnl_dict))     
            
        if self.code_jrnl_cash:
            jrnl_dict = {
                'name': self.name_jrnl_cash,
                'type': 'cash',
                'code': self.code_jrnl_cash,
                'sequence_id':self._create_sequence(self.code_jrnl_cash + '-' + _('Sequence'), self.seq_jrnl_cash, bu.company_id.id),
                'business_unit_id': bu.id,
                'company_id': bu.company_id.id            
                }
            vals.setdefault('journal_ids',[]).append((0,0,jrnl_dict))     

        if self.code_jrnl_bank:
            jrnl_dict = {
                'name': self.name_jrnl_bank,
                'type': 'bank',
                'code': self.code_jrnl_bank,
                'sequence_id':self._create_sequence(self.code_jrnl_bank + '-' + _('Sequence'), self.seq_jrnl_bank, bu.company_id.id),
                'business_unit_id': bu.id,
                'company_id': bu.company_id.id            
                }
            vals.setdefault('journal_ids',[]).append((0,0,jrnl_dict))
                
        if vals:
            vals['initialized'] = True
            bu.sudo().write(vals)                
        return True
