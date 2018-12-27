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
			"get_query": () => {
				return {
					filters: { "name": ["in", ["Serial No", "Batch"]] }
				}
			},
			"on_change": () => {
				frappe.query_report.set_filter_value("link_name", null);
			},
			"reqd": 1
		},
		{
			"fieldname": "link_name",
			"label": __("Serial / Batch"),
			"fieldtype": "Dynamic Link",
			"options": "link_doctype",
			"reqd": 1
		},
	]
}
