# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document

#BASE_URL, AUTH, PARAMS = get_metrc_config()

class LabTest(Document):
	def on_submit(self):
		results = []
		for res in self.results:
			results.append({
				"LabTestTypeName": res.lab_test_type_name,
				"Quantity": res.quantity,
				"Passed": res.passed,
				"Notes": res.notes
			})
		
		data = [
			{
				"Label": self.label,
				"ResultDate": self.result_date,
				"Results": results
			}
		]
		
		

def get_metrc_config():
	metrc_settings = frappe.get_single("Metrc API Settings")

	base_url = metrc_settings.url
	auth = (metrc_settings.api_key, metrc_settings.user_key)
	params = {"licenseNumber": metrc_settings.lab_test}

	return base_url, auth, params
