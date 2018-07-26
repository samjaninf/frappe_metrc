# Copyright (c) 2013, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from frappe.utils.background_jobs import enqueue

def execute(filters=None):
	columns, data = [], []

	if not filters:
		return columns, data

	if not filters.get("package_id"):
		return columns, data

	selected_doctype = filters.get("link_doctype")
	columns = get_columns(selected_doctype)

	if selected_doctype == "Serial No":
		# What the fuck
		results = get_serial_nos(filters.get("package_id"), [])
		if results:
			for result in results[:-1]:
				sle_list = frappe.get_all("Stock Ledger Entry", filters={"serial_no": [
					"like", "%{}%".format(result)]}, fields=["item_code", "batch_no", "serial_no", "warehouse", "posting_date", "voucher_type", "voucher_no"])
				for sle in sle_list:
					data.append([sle.item_code, sle.batch_no, sle.serial_no, sle.warehouse,
										sle.voucher_type, sle.voucher_no, sle.posting_date])

	# Much less fucky
	elif selected_doctype == "Batch":
		results = [result for result in recursively_get_links(filters.get("package_id"), []) if result is not None]

		if results:
			sle_list = frappe.get_all("Stock Ledger Entry", filters={"batch_no": [
				"in", results]}, fields=["item_code", "batch_no", "serial_no", "warehouse", "posting_date", "voucher_type", "voucher_no"])
			for sle in sle_list:
				data.append([sle.item_code, sle.batch_no, sle.serial_no, sle.warehouse,
							 sle.voucher_type, sle.voucher_no, sle.posting_date])

	return columns, data


def get_serial_nos(source_serial_no, serial_nos):
	stock_entries = frappe.get_all("Stock Entry Detail", filters={"serial_no": [
		"like", "%{}%".format(source_serial_no)]}, fields=["parent"])

	for se in stock_entries:
		se_doc = frappe.get_doc("Stock Entry", se.parent)
		for item in se_doc.items:
			if item.serial_no:
				serials = item.serial_no.split("\n")

				for serial_no in serials:
					if serial_no not in serial_nos:
						serial_nos.extend(serials)
						get_serial_nos(serial_no, serial_nos)

	return serial_nos


def recursively_get_links(batch_no, batch_list):
	link_info = {
		'Stock Entry': {
			'child_doctype': 'Stock Entry Detail',
			'fieldname': ['batch_no']
		}
	}

	results = get_linked_docs("Batch", batch_no,
							  linkinfo=link_info)

	for doctype, documents in results.iteritems():
		for document in documents:
			if document.get("docstatus") == 1 and batch_no not in batch_list:
				batch_list.append(batch_no)
				se = frappe.get_doc("Stock Entry", document.get("name"))
				for item in se.items:
					if batch_no != item.batch_no:
						recursively_get_links(item.batch_no, batch_list)

	return batch_list


def get_columns(selected_doctype):
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
				"width": 90
			},
            {
				"fieldname": "serial_no",
				"label": _("Serial No"),
				"fieldtype": "Serial",
				"options": "Data",
				"width": 90
			},
			{
				"fieldname": "warehouse",
				"label": _("Warehouse"),
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 90
			},
			{
				"fieldname": "activity_doctype",
				"label": _("Activity DocType"),
				"fieldtype": "Link",
				"options": "DocType",
				"width": 90
			},
			{
				"fieldname": "activity_document",
				"label": _("Activity Document"),
				"fieldtype": "Dynamic Link",
				"options": "activity_doctype",
				"width": 90
			},
			{
				"fieldname": "posting_date",
				"label": _("Posting Date"),
				"fieldtype": "Date",
				"width": 90
			},
		]
