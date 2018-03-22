
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
def material_request_data(self,Document):
	frappe.msgprint("Test")
	query = frappe.db.sql("""select name, status
			from `tabMaterial Request` WHERE material_request='{self.material_request}' """,as_dict=1)
	for data in query :
		new_data += data
		frappe.msgprint(new_data)
	self.doc_details="test"

