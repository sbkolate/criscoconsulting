# # Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	validate_filters(filters)
	columns = get_columns()
	stock = get_total_stock(filters)
	new_data=[]
	for i in stock:
		# print("\n",i[3])
		i2=0
		i3=0
		i6=0
		i5=0
		i9=0
		i8=0
		if i[3] == None:
			i3=0
		else:
			i3=i[3]
		if i[3] == None:
			i2=0
		else:
			i2=i[3]

		if i[6] == None:
			i6=0
		else:
			i6=i[6]
		if i[5] == None:
			i5=0
		else:
			i5=i[5]

		if i[9] == None:
			i9=0
		else:
			i9=i[9]
		if i[8] == None:
			i8=0
		else:
			i8=i[8]

		i10 = i2+i5+i8



		new_data.append(['i[0]',i[1],i2,i3,i[4],i5,i6,i[7],i8,i9,i10])
	

	stock=new_data
	return columns, stock

def get_columns():
	columns = [
		_("Item Code") + ":Link/Item:150",
		("Main - Riyadh") + ":Link/Item:150",
		_("Stock-Riyadh") + ":Float:120",
		("Valuation Rate MR") + ":Float:120",
		_("Main-Al-Khobar - SAM") + ":Data:150",
		_("Stock-MAK") + ":Float:120",
		("Valuation Rate MAK") + ":Float:120",
		_("Main -Jeddah - SAM") + ":Data:150",
		_("Stock-MJ1") + ":Float:120",
		("Valuation Rate MJ") + ":Float:120",
		_("Total QTY") + ":Float:120",


	]

	return columns

def get_total_stock(filters):
	# frappe.db.sql(""" UPDATE tabBin SET actual_qty = 0 WHERE actual_qty=''""")
	# frappe.db.sql(""" UPDATE tabBin SET actual_qty = 0 WHERE actual_qty=''""")
	conditions = ""
	columns = ""

	if filters.get("group_by") == "Warehouse":
		conditions += " GROUP BY ledger.warehouse, item.item_code"
		columns += "'' as company, ledger.warehouse"
	else:
		conditions += " GROUP BY ledger.warehouse, item.item_code"
		columns += " warehouse.company, '' as warehouse"

	return frappe.db.sql("""select
			tb.item_code,'Main-Riyadh - SAM',
			CASE
			    WHEN 1=1
			    THEN (select b.actual_qty
			    	from tabBin b 
			    	where b.warehouse = 'Main-Riyadh - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w1_r1,
			CASE
			    WHEN 1=1
			    THEN (select b.valuation_rate
			    	from tabBin b 
			    	where b.warehouse = 'Main-Riyadh - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w20,
			'Main-Al-Khobar - SAM',
			CASE
			    WHEN 1=1
			    THEN (select b.actual_qty 
			    	from tabBin b 
			    	where b.warehouse = 'Main-Al-Khobar - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w1,
			CASE
			    WHEN 1=1
			    THEN (select b.valuation_rate
			    	from tabBin b 
			    	where b.warehouse = 'Main-Al-Khobar - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w21,
			'Main-Jeddah - SAM',
			CASE
			    WHEN 1=1
			    THEN (select b.actual_qty 
			    	from tabBin b where b.warehouse = 'Main-Jeddah - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w14,
			CASE
			    WHEN 1=1
			    THEN (select b.valuation_rate
			    	from tabBin b 
			    	where b.warehouse = 'Main-Jeddah - SAM' 
			    	and b.item_code=tb.item_code limit 1)
			    ELSE 0
			END as act_w22
			from tabBin tb group by tb.item_code""")


def validate_filters(filters):
	pass
