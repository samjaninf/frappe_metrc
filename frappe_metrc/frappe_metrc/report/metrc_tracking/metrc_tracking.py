# Copyright (c) 2013, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe.desk.query_report import get_linked_doctypes
from frappe.utils.background_jobs import enqueue


def execute(filters=None):
	columns, data = [], []

	if not filters:
		return columns, data

	if not filters.get("package_id"):
		return columns, data

	if filters.get("link_doctype") == "Serial No":
		columns = ["Serial No:Link/Serial No:120", "Item:Link/Item:240",
					"Warehouse:Link/Warehouse:120", "Activity Document:Link/Stock Entry:120", "Creation Date"]

		# What the fuck
		serial_nos = get_serial_nos(filters.get("package_id"), [])
		serial_nos = filter(bool, serial_nos)
		serial_nos = list(set(serial_nos))
		serial_nos = reversed(sorted(serial_nos, key=lambda x: frappe.db.get_value("Serial No", x, "creation")))

		for serial_no in serial_nos:
			serial_no = frappe.get_doc("Serial No", serial_no)

			if not serial_no.warehouse or not data:
				data.append([serial_no.name, serial_no.item_name, serial_no.warehouse,
							serial_no.purchase_document_no, frappe.utils.format_datetime(serial_no.creation)])

	# Much less fucky
	if filters.get("link_doctype") == "Batch":
		columns = ["Batch:Link/Batch:120", "Quantity::100", "Item:Link/Item:240",
					"Warehouse:Link/Warehouse:120", "Activity Document:Link/Stock Entry:120", "Creation Date"]

		batch = frappe.get_doc("Batch", filters.get("package_id"))
		batch_details = get_batch_qty(batch.name, item_code=batch.item)

		for batch_detail in batch_details:
			data.append([batch.name, batch_detail["qty"], batch.item, batch_detail["warehouse"],
						"", frappe.utils.format_datetime(batch.creation)])

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
