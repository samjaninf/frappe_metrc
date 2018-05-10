# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests

class Strain(Document):
	def validate(self):
		if not self.indica_percentage + self.sativa_percentage == 100:
			frappe.throw("Indica Percentage and Sativa Percentage combined must be 100%.")
		
		metrc_settings = frappe.get_single("Metrc API Settings")
		auth=(metrc_settings.api_key, metrc_settings.user_key)
		params={"licenseNumber": metrc_settings.strain}
		
		if not self.strain_id:
			#Create Strain in Metrc and assign ID
			data=[{
				"Name": self.strain_name,
				"TestingStatus": self.testing_status,
				"ThcLevel": self.thc_level,
				"CbdLevel": self.cbd_level,
				"IndicaPercentage": self.indica_percentage,
				"SativaPercentage": self.sativa_percentage
			}]
			post_url = metrc_settings.url + "/strains/v1/create"
			#metrc will return a 200 if all is good
			#it won't send the id of the strain; you need to guess that out
			requests.post(url=post_url, auth=auth, params=params, json=data)

			#Try to find if the strain id was assigned 
			get_url = metrc_settings.url + "/strains/v1/active"
			response = requests.get(url=get_url, auth=auth, params=params)
			for strain in response.json():
				if strain.get("Name") == self.strain_name:
					self.strain_id = strain.get("Id")
		else:
			#use the update API to update the object if strain id exists
			data=[{
				"Id": self.strain_id,
				"Name": self.strain_name,
				"TestingStatus": self.testing_status,
				"ThcLevel": self.thc_level,
				"CbdLevel": self.cbd_level,
				"IndicaPercentage": self.indica_percentage,
				"SativaPercentage": self.sativa_percentage
			}]
			post_url = metrc_settings.url + "/strains/v1/update"
			requests.post(url=post_url, auth=auth, params=params, json=data)

	def on_trash(self):
		metrc_settings = frappe.get_single("Metrc API Settings")
		auth=(metrc_settings.api_key, metrc_settings.user_key)
		params={"licenseNumber": metrc_settings.strain}
		del_url = metrc_settings.url + "/strains/v1/" + self.strain_id
		requests.delete(url=del_url, auth=auth, params=params)
