frappe.ui.form.on("Customer", "refresh", function(frm) {cur_frm.fields_dict['customer_group'].get_query = function(doc) {
        return {
            filters: {
                'is_group': 0
           }
		
        }
    };
});