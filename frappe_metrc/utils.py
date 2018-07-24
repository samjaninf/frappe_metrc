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
import random
from faker import Faker


def get_metrc(license_type):
	metrc_settings = frappe.db.get_singles_dict("Metrc API Settings")
	license = metrc_settings.get(license_type)

	return METRC(metrc_settings.api_key, metrc_settings.user_key, license, url=metrc_settings.url)


def add_comment_to_batch(stock_entry, method):
	for item in stock_entry.items:
		if item.batch_no:
			if item.s_warehouse:
				comment_text = "{qty} {uom} consumed by {stock_entry}".format(qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)
			elif item.t_warehouse:
				comment_text = "{qty} {uom} created from {stock_entry}".format(
					qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)

			batch_doc = frappe.get_doc("Batch", item.batch_no)
			print(comment_text)
			comment = batch_doc.add_comment(comment_type="Comment", text=comment_text)
			comment.comment_type = "Info"
			comment.save()

	frappe.db.commit()


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

		if item.s_warehouse and item.batch_no:
			package_ingredients.append({
				"Package": item.batch_no,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
			})

	if payload:
		payload["Ingredients"] = package_ingredients
		send_request("/packages/v1/create", [payload], stock_entry.doctype, stock_entry.name)


def create_transfers():

	faker = Faker()
	shipper_licenses = ["C10-18-0000005-TEMP",
                  "C10-18-0000004-TEMP",
                  "M10-18-0000354-TEMP",
                  "A10-18-0000301-TEMP",
                  "C10-18-0000001-TEMP",
                  "C10-18-0000002-TEMP",
                  "C10-18-0000003-TEMP",
                  "M10-18-0000338-TEMP",
                  "M10-18-0000421-TEMP",
                  "A10-18-0000368-TEMP",
                  "A10-18-0000296-TEMP",
                  "A10-18-0000367-TEMP",
                  "A10-18-0000366-TEMP",
                  "A10-18-0000365-TEMP",
                  "M10-18-0000417-TEMP",
                  "M10-18-0000411-TEMP",
                  "A10-18-0000360-TEMP",
                  "M10-18-0000302-TEMP",
                  "A10-18-0000258-TEMP"]

	shipper_names = ["Hueneme Patient Consumer Collective, LLC.",
                     "Southern California Collective",
                     "Ketama Cooperative",
                     "Sunrise Caregiver Foundation Inc.",
                     "CANA",
                     "K.U.S.H. Alley Collective, Inc.",
                     "DBO Investments PH, LLC",
                     "The Healing Center Needles",
                     "Venice Caregiver Foundation, Inc.",
                     "East Bay Therapeutics",
                     "US BLOOM COLLECTIVE",
                     "CannaBoutique Dispensary LLC",
                     "WE CARE CAT CITY",
                     "Valley Greens Retail Outlet, LP",
                     "CANOPY CLUB, INC.",
                     "The Bud Farmacy Corporation",
                     "Accensus Group, LLC",
                     "All Natural Inc.",
                     "Virgil Grant",
                     "MISSION HERBAL CARE INC"]





	for x in range(1):
		td = frappe.new_doc("Transfer")
		td.manifest_no = random.randint(1000000001, 10000000000)
		td.recieved_on = faker.past_datetime(start_date="-30d", tzinfo=None)
		td.shipper_license = random.choice(shipper_licenses)
		td.shipper_name = random.choice(shipper_names)
		if random.randint(1,10) < 9:
			td.entered_in_metrc = 1
		td.save()
		frappe.db.commit()


