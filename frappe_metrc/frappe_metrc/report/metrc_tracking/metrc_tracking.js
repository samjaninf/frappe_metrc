// Copyright (c) 2016, Neil Lasrado and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Metrc Tracking"] = {
    "filters": [
	        {
	            "fieldname":"serial_no",
	            "label": __("Serial No"),
	            "fieldtype": "Link",
	            "options": "Serial No"
	        }
	]
}
