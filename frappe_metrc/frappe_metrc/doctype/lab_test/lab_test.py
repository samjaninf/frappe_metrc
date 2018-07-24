# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document
from frappe_metrc.utils import get_metrc

metrc = get_metrc("lab_test")

class LabTest(Document):
	def on_submit(self):
		results = []
		for result in self.results:
			results.append({
				"LabTestTypeName": result.lab_test_type,
				"Quantity": result.quantity,
				"Passed": result.passed,
				"Notes": result.notes
			})
		
		data = [
			{
				"Label": self.label,
				"ResultDate": self.result_date,
				"Results": results
			}
		]

		response = metrc.post("/labtests/v1/record", data)
		if response != "Success":
			frappe.throw(response)


		
		


