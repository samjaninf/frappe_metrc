# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from frappe.model.document import Document
from frappe_metrc.utils import get_metrc


class APIRequestLog(Document):

	def before_insert(self):
		self.send_request()

	def retry(self):
		self.send_request()

	def send_request(self):
		# license_type = frappe.scrub(self.get("reference_document"))
		license_type = "room"
		client = get_metrc(license_type)

		response = client.post(
			self.endpoint, data=json.loads(self.request_body))

		self.response_body = response.text
		self.response_code = response.status_code
