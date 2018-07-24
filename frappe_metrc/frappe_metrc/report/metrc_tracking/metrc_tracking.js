// Copyright (c) 2016, Neil Lasrado and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Metrc Tracking"] = {
    "filters": [
		{
			"fieldname": "link_doctype",
			"label": __("Select..."),
			"fieldtype": "Link",
			"options": "DocType",
			"default": "Batch",
			"get_query": function () {
				return {
					filters: { "name": ["in", ["Serial No", "Batch"]] }
				}
			},
			"reqd": 1
		},
		{
			"fieldname": "package_id",
			"label": __("Serial / Batch"),
			"fieldtype": "Dynamic Link",
			"options": "link_doctype"
		},
	]
}
