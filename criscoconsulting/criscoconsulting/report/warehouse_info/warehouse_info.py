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
	for item in stock:
		stock_riyadh=0
		valuation_rate_riyadh=0
		valuation_rate_mak=0
		stock_mak=0
		valuation_rate_mj=0
		stock_mj=0
		if item[3] == None:
			valuation_rate_riyadh=0
		else:
			valuation_rate_riyadh=item[3]
		if item[3] == None:
			stock_riyadh=0
		else:
			stock_riyadh=item[3]

		if item[6] == None:
			valuation_rate_mak=0
		else:
			valuation_rate_mak=item[6]
		if item[5] == None:
			stock_mak=0
		else:
			stock_mak=item[5]

		if item[9] == None:
			valuation_rate_mj=0
		else:
			valuation_rate_mj=item[9]
		if item[8] == None:
			stock_mj=0
		else:
			stock_mj=item[8]

		total_qty = stock_riyadh+stock_mak+stock_mj

		new_data.append([item[0],
			item[1],stock_riyadh,valuation_rate_riyadh,
			item[4],stock_mak,valuation_rate_mak,
			item[7],stock_mj,valuation_rate_mj,
			total_qty])

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
