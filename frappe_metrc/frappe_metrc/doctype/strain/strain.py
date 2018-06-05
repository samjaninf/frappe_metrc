# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe import _
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.utils import get_metrc

metrc = get_metrc("strain")

class Strain(Document):
	def validate(self):
		pass
		# self.create_or_update_strain()
		# self.check_strain()

	def after_rename(self, old, new, merge=False):
		self.create_or_update_strain()

	def create_or_update_strain(self):
		if self.indica_percentage and self.sativa_percentage:
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
			metrc.post("/strains/v1/create", data)
		else:
			# use the update API to update the object if strain id exists
			data[0].update({"Id": self.strain_id})
			metrc.post("/strains/v1/update", data)

	def check_strain(self):
		# Try to find if the strain id was assigned
		strains = metrc.get("/strains/v1/active")

		for strain in strains:
			if strain.get("Name") == self.strain_name:
				self.strain_id = strain.get("Id")

	def on_trash(self):
		metrc.delete("/strains/v1/" + self.strain_id)
