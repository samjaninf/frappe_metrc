# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe_metrc.utils import get_metrc

metrc = get_metrc("plant_batch")

class PlantBatch(Document):

	def validate(self):
		# self.create_or_update_plant_batch()
		self.check_plant_batch()

	def after_rename(self, old, new, merge=False):
		self.create_or_update_plant_batch()

	def create_or_update_plant_batch(self):
		data = [
                    {
                        "Name": self.batch_name,
                        "Type": self.type,
                        "Count": self.count,
                        "Strain": self.strain,
                        "ActualDate": self.actual_date
                    }
		]

		if not self.batch_id:
			# Create Room in Metrc and assign ID
			response = metrc.post("/plantbatches/v1/createplantings", data)
			if response != "Success":
				frappe.throw(response)
		else:
			data[0].update({"Id": self.batch_id})
			# use the update API to update the object if room id exists
			response = metrc.post("/plantbatches/v1/update", data)
			if response != "Success":
				frappe.throw(response)

	def check_plant_batch(self):
		# Try to find if the room id was assigned
		plant_batch = metrc.get("/plantbatches/v1/{}".format(self.batch_id))
		self.batch_id = plant_batch.get("Id")
		self.room = plant_batch.get("RoomName")
		self.strain = plant_batch.get("StrainName")
		self.count = plant_batch.get("Count")

	def on_trash(self):
		data = [{
			"Id" : self.batch_id,
			"Count" : self.count,
			"ActualDate" : frappe.utils.today(),
			"ReasonNote" : "Just Cause"
		}]
		metrc.post("/plantbatches/v1/destroy", data)
