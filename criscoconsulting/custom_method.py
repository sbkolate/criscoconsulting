
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
def material_request_data(self,Document):
	# frappe.msgprint("Test")
	query = frappe.db.sql("""select name, material_transfer_type
			from `tabMaterial Transfer` 
			WHERE material_request='{0}' """.format(self.material_request),as_dict=1)
	
	doc_details=""
	for i in query :
		doc_details += i.name+" - "+i.material_transfer_type+" \n"
		
	self.doc_details=doc_details

