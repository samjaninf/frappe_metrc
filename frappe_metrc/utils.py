# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document
import json
from frappe_metrc.metrc.request import METRC
from frappe.utils.background_jobs import enqueue

def get_metrc(license_type):
	metrc_settings = frappe.db.get_singles_dict("Metrc API Settings")
	license = metrc_settings.get(license_type)
	return METRC(metrc_settings.api_key,  metrc_settings.user_key, license, url=metrc_settings.url)

def _send_request(endpoint, data):
	request = frappe.new_doc("API Request Log")
	request.endpoint = endpoint
	request.request_body = json.dumps(data)
	request.insert()
	frappe.db.commit()

def send_request(endpoint, data):
	enqueue(_send_request, endpoint=endpoint, data=data)

def create_package(doc, method):
	if doc.purpose != "Manufacture":
		return

	payload = []