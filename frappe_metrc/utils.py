# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import requests

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from frappe_metrc.metrc.request import METRC


def get_metrc(license_type):
	metrc_settings = frappe.db.get_singles_dict("Metrc API Settings")
	license = metrc_settings.get(license_type)

	return METRC(metrc_settings.api_key, metrc_settings.user_key, license, url=metrc_settings.url)


def add_comment_to_batch(stock_entry, method):
	for item in stock_entry.items:
		# comment_text =

		stock_entry.add_comment(comment_type="Info")


def _send_request(endpoint, data, ref_dt=None, ref_dn=None):
	request = frappe.new_doc("API Request Log")
	request.endpoint = endpoint
	request.request_body = json.dumps(data)
	request.reference_doctype = ref_dt
	request.reference_document = ref_dn

	request.insert()
	frappe.db.commit()


def send_request(endpoint, data, ref_dt=None, ref_dn=None):
	enqueue(_send_request, endpoint=endpoint, data=data, ref_dt=ref_dt, ref_dn=ref_dn)


def create_package(stock_entry, method):
	if stock_entry.purpose != "Manufacture":
		return

	package_ingredients = []

	for item in stock_entry.items:
		# TODO: only run code if items are cannabis products
		if item.t_warehouse:
			payload = {
				"Tag": item.batch_no,
				"Item": item.item_code,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
				"ActualDate": stock_entry.posting_date,
				"Ingredients": []
			}

		if item.s_warehouse:
			package_ingredients.append({
				"Package": item.batch_no,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
			})

	if payload:
		payload["Ingredients"] = package_ingredients
		send_request("/packages/v1/create", [payload], stock_entry.doctype, stock_entry.name)
