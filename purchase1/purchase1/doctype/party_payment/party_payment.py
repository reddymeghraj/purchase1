# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PartyPayment(Document):
	def on_submit(self):
		q2=frappe.db.sql("""select * from `tabPayment` where party=%s""",self.party)
		if q2:
			q1=frappe.db.sql("""update `tabPayment` set payment=payment-%s where party=%s""",(self.paid_amount,self.party))
			if self.payment_mode=='Cash':
				que=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
				if que:
					n=int(que)+1
					que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))
				else:	
					n=1
					que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))	
			else:
				qu=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Info`""")[0][0]
				if qu:
					n1=int(qu)+1
					qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
				else:
					n1=1
					qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
		else:
			q4=frappe.db.sql("""select MAX(cast(name as int)) from `tabPayment`""")[0][0]
			if q4:
				name=int(q4)+1
				q1=frappe.db.sql("""insert into `tabPayment` set name=%s,party=%s,payment=-1*%s""",(name,self.party,self.paid_amount))
				if self.payment_mode=='Cash':
					que=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
					if que:
						n=int(que)+1
						que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))
					else:	
						n=1
						que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))	
				else:
					qu=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Info`""")[0][0]
					if qu:
						n1=int(qu)+1
						qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
					else:
						n1=1
						qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
			else:
				name=1	
	    		q1=frappe.db.sql("""insert into `tabPayment` set name=%s,party=%s,payment=-1*%s""",(name,self.party,self.paid_amount))
	    		if self.payment_mode=='Cash':
	    			que=frappe.db.sql("""select max(cast(name as int)) from `tabCash`""")[0][0]
	    			if que:
	    				n=int(que)+1
	    				que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))
	    			else:
	    				n=1
	    				que1=frappe.db.sql("""insert into `tabCash` set name=%s,party=%s,party_name=%s,amount=%s,date=%s,transaction='2',description='Purchase Amount'""",(n,self.party,self.party_name,self.paid_amount,self.date))
	    		else:
	    			qu=frappe.db.sql("""select max(cast(name as int)) from `tabCheque Info`""")[0][0]
	    			if qu:
	    				n1=int(qu)+1
	    				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
	    			else:
	    				n1=1
	    				qu1=frappe.db.sql("""insert into `tabCheque Info` set name=%s,party=%s,party_name=%s,bank=%s,bank_name=%s,cheque_no=%s,amount=%s,date=%s,status='Uncleared',transaction='2',description='Purchase Amount'""",(n1,self.party,self.party_name,self.bank,self.bank_name,self.cheque_no,self.paid_amount,self.date))
	    				
	    				
@frappe.whitelist()
def get_amount(party):
	query=frappe.db.sql("""select payment from `tabPayment` where party=%s""",party)
	if query:
		return query[0][0]
	else:
		return ''
		