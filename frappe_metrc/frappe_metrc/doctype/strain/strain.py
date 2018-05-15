# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe import _
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.utils import get_metrc_config

class Strain(Document):
	BASE_URL, AUTH, PARAMS = get_metrc_config()

	def validate(self):
		self.create_or_update_strain()
		self.check_strain()

	def create_or_update_strain(self):
		if not self.indica_percentage + self.sativa_percentage == 100:
			frappe.throw(_("Indica Percentage and Sativa Percentage combined must be 100%."))

		data = [
			{
				"Name": self.strain_name,
				"TestingStatus": self.testing_status,
				"ThcLevel": self.thc_level,
				"CbdLevel": self.cbd_level,
				"IndicaPercentage": self.indica_percentage,
				"SativaPercentage": self.sativa_percentage
			}
		]

		if not self.strain_id:
			# Create Strain in Metrc and assign ID
			url = BASE_URL + "/strains/v1/create"
		else:
			# use the update API to update the object if strain id exists
			data[0].update({"Id": self.strain_id})

			url = BASE_URL + "/strains/v1/update"

		# metrc will return a 200 if all is good
		# it won't send the id of the strain; you need to guess that out
		requests.post(url=url, auth=AUTH, params=PARAMS, json=data)

	def check_strain(self):
		# Try to find if the strain id was assigned
		url = BASE_URL + "/strains/v1/active"
		response = requests.get(url=url, auth=AUTH, params=PARAMS)

		for strain in response.json():
			if strain.get("Name") == self.strain_name:
				self.strain_id = strain.get("Id")

	def on_trash(self):
		url = BASE_URL + "/strains/v1/" + self.strain_id
		requests.delete(url=url, auth=AUTH, params=PARAMS)
