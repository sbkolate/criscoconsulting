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
		new_data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
	
	new_list = []

	for i in new_data:
		new_list.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])

	stock=new_list
	return columns, new_data

def get_columns():
	columns = [
		_("Item Code") + ":Link/Item:150",
		("Main - Riyadh") + ":Link/Item:150",
		_("Stock-Riyadh") + ":Float:120",
		("Valuation Rate") + ":Float:120",
		_("Main-Al-Khobar - SAM") + ":Data:150",
		_("Stock-MAK") + ":Float:120",
		("Valuation Rate") + ":Float:120",
		_("Main -Jeddah - SAM") + ":Data:150",
		_("Stock-MJ1") + ":Float:120",
		("Valuation Rate") + ":Float:120",
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
			END as act_w22,
			CASE
			    WHEN 1=1
			    THEN (select sum(b.actual_qty)
			    	from tabBin b 
			    	where b.item_code=tb.item_code
			    	and (b.warehouse = 'Main-Al-Khobar - SAM' 
			    	OR b.warehouse = 'Main-Riyadh - SAM' 
			    	or b.warehouse = 'Main-Jeddah - SAM'))
			    ELSE 0
			END as act_w11
			from tabBin tb group by tb.item_code""")


def validate_filters(filters):
	pass
