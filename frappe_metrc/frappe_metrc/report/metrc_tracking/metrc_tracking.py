# Copyright (c) 2013, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.desk.form.linked_with import get_linked_docs


def execute(filters=None):
	columns, data = [], []

	if not filters:
		return columns, data

	columns = get_columns()
	data = get_data(filters.get("link_doctype"), filters.get("link_name"))

	return columns, data


def get_data(link_doctype, link_name, data=None, completed=None):
	if not completed:
		completed = []

	if not data:
		data = []

	link_doc = frappe.get_doc(link_doctype, link_name)
	if link_doctype == "Serial No":
		source_doc = frappe.get_doc(link_doc.purchase_document_type, link_doc.purchase_document_no)
	elif link_doctype == "Batch":
		source_doc = frappe.get_doc(link_doc.reference_doctype, link_doc.reference_name)

	supplier = source_doc.supplier if source_doc.doctype == "Purchase Receipt" else ""

	for item in source_doc.get("items", []):
		if source_doc.doctype == "Purchase Receipt":
			warehouse = item.warehouse
		elif source_doc.doctype == "Stock Entry":
			warehouse = item.t_warehouse

		if item.get("t_warehouse") or item.get("warehouse"):
			completed.append(link_name)
			data.append({
				"item_code": item.item_code,
				"serial_no": link_name if item.serial_no else "",
				"batch_no": link_name if item.batch_no else "",
				"qty": item.qty,
				"stock_uom": item.stock_uom,
				"warehouse": warehouse,
				"date": source_doc.posting_date,
				"supplier": supplier,
				"activity_doctype": source_doc.doctype,
				"activity_document": source_doc.name
			})
		elif item.get("s_warehouse"):
			if item.serial_no and item.serial_no not in completed:
				data = get_data("Serial No", item.serial_no, data, completed)
			elif item.batch_no and item.batch_no not in completed:
				data = get_data("Batch", item.batch_no, data, completed)

	return data


def get_columns():
	return [
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 90
		},
		{
			"fieldname": "batch_no",
			"label": _("Batch No"),
			"fieldtype": "Link",
			"options": "Batch",
			"width": 100
		},
		{
			"fieldname": "serial_no",
			"label": _("Serial No"),
			"fieldtype": "Serial",
			"options": "Data",
			"width": 110
		},
		{
			"fieldname": "qty",
			"label": _("Quantity"),
			"fieldtype": "Float",
			"width": 90
		},
		{
			"fieldname": "stock_uom",
			"label": _("Unit"),
			"fieldtype": "Link",
			"options": "UOM",
			"width": 90
		},
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150
		},
		{
			"fieldname": "date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 90
		},
		{
			"fieldname": "activity_doctype",
			"label": _("Activity Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"width": 90
		},
		{
			"fieldname": "activity_document",
			"label": _("Activity Document"),
			"fieldtype": "Dynamic Link",
			"options": "activity_doctype",
			"width": 150
		},
		{
			"fieldname": "supplier",
			"label": _("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 100
		}
	]
