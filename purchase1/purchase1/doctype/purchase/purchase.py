# Copyright (c) 2013, wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Purchase(Document):
	def on_submit(self):
		q2=frappe.db.sql("""select * from `tabPayment` where party=%s""",self.party)
		if q2:
			q1=frappe.db.sql("""update `tabPayment` set payment=payment+%s where party=%s""",(self.total_amount,self.party))
		else:
			q4=frappe.db.sql("""select MAX(cast(name as int)) from `tabPayment`""")[0][0]
			if q4:
				name=int(q4)+1
				q1=frappe.db.sql("""insert into `tabPayment` set name=%s,party=%s,payment=%s""",(name,self.party,self.total_amount))
			else:
				name=1	
	    		q1=frappe.db.sql("""insert into `tabPayment` set name=%s,party=%s,payment=%s""",(name,self.party,self.total_amount))
			
		for d in self.get('purchase_item'):
			query=frappe.db.sql("""select * from `tabStock` where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s""",(d.brand,d.cloth_type,d.category,d.color,d.size))
			if query:
				query1=frappe.db.sql("""update `tabStock` set quantity=quantity+%s  where brand=%s and cloth_type=%s and category=%s and color=%s and size=%s""",(d.quantity,d.brand,d.cloth_type,d.category,d.color,d.size));
			else:
				q=frappe.db.sql("""select MAX(cast(name as int)) from `tabStock`""")[0][0]
				if q:
					name=int(q)+1
				else:
					name=1	
				query1=frappe.db.sql("""insert into `tabStock` set name=%s,brand=%s,brand_name=%s,cloth_type=%s,clothtype_name=%s,category=%s,category_name=%s,color=%s,color_name=%s,size=%s,size_value=%s,quantity=%s""",(name,d.brand,d.brand_name,d.cloth_type,d.clothtype_name,d.category,d.category_name,d.color,d.color_name,d.size,d.size_value,d.quantity));		
@frappe.whitelist()
def get_brand_name(brand):
	query=frappe.db.sql("""select brand_name from `tabAdd Brand` where name=%s""",brand)
	return query[0][0]
@frappe.whitelist()
def get_clothtype_name(cloth_type):
	query=frappe.db.sql("""select cloth_type from `tabAdd Clothtype` where name=%s""",cloth_type)
	return query[0][0]
@frappe.whitelist()
def get_category_name(category):
	query=frappe.db.sql("""select category from `tabAdd Category` where name=%s""",category)
	return query[0][0]
@frappe.whitelist()
def get_color_name(color):
	query=frappe.db.sql("""select color from `tabAdd Color` where name=%s""",color)
	return query[0][0]
@frappe.whitelist()
def get_size_value(size):
	query=frappe.db.sql("""select size from `tabAdd Size` where name=%s""",size)
	return query[0][0]	
@frappe.whitelist()
def generate_barcode(size):
	q=frappe.db.sql("""select max(name) from `tabPdetails`""")
	if q[0][0]:
		q1=frappe.db.sql("""select max(item_code) from `tabItem`""")
		delemiter='I'
		barcode=q1[0][0].split(delemiter)
		item_code1=int(barcode[1])+1
		if item_code1<10:
			item_code='PI0000000000'+str(item_code1)
		if item_code1>10 and item_code1<100:
			item_code='PI000000000'+str(item_code1)
		if item_code1>100 and item_code1<1000:
			item_code='PI00000000'+str(item_code1)
		if item_code1>1000 and item_code1<10000:
			item_code='PI0000000'+str(item_code1)
		if item_code1>10000 and item_code1<100000:
			item_code='PI000000'+str(item_code1)	
		if item_code1>100000 and item_code1<1000000:
			item_code='PI00000'+str(item_code1)	
		if item_code1>1000000 and item_code1<10000000:
			item_code='PI0000'+str(item_code1)	
		if item_code1>10000000 and item_code1<100000000:
			item_code='PI000'+str(item_code1)
		if item_code1>100000000 and item_code1<1000000000:
			item_code='PI00'+str(item_code1)		
		if item_code1>1000000000 and item_code1<10000000000:
			item_code='PI0'+str(item_code1)
		if item_code1>10000000000 and item_code1<100000000000:
			item_code='PI'+str(item_code1)	
	else:
		item_code='PI00000000001'
	qs=frappe.db.sql("""select max(cast(name as int)) from `tabItem`""")[0][0]
	if qs:
		name=int(qs)+1
		q2=frappe.db.sql("""insert into `tabItem` set name=%s,item_code=%s""",(name,item_code))
	else:
		name=1
		q2=frappe.db.sql("""insert into `tabItem` set name=%s,item_code=%s""",(name,item_code))	
	options=[]
	options.append(item_code)	
	query=frappe.db.sql("""select size from `tabAdd Size` where name=%s""",size)
	options.append(query[0][0])	
	return options;	
@frappe.whitelist()
def create_barcode(bar):
	query=frappe.db.sql("""select * from `tabPdetails` where barcode=%s""",bar)
	if query:
		barcode_img = """<html>
		<div id='printable'>
		<table>
		<tr>
		<td >
			<img src=assets/image/"""+bar+""".svg/>"""
		"""</td>
		</tr>
		</table>
		</div>
		</html>"""	
		return barcode_img;
	else:	
		import barcode
		from barcode.writer import ImageWriter
		code39 = barcode.get('code39', bar, writer=ImageWriter)
  		fullname = code39.save('assets/image/'+bar)
  		barcode_img = """<html>
  		<div id='printable'>
		<table style="width: 100%; table-layout: fixed;">
		<tr>
		<td style="width:510px">
			<img src=assets/image/"""+bar+""".svg width="200px"/>"""
		"""</td>
		</tr>
		</table>
		</div>
		</html>"""			
		return barcode_img;	
@frappe.whitelist()
def rem_item_code():
	q=frappe.db.sql("""select max(name) from `tabPdetails`""")
	q1=frappe.db.sql("""select max(item_code) from `tabItem`""")
	if q[0][0]<q1[0][0]:
		q2=frappe.db.sql("""delete from `tabItem` where item_code>%s""",q[0][0])
		
