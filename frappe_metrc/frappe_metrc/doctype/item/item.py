# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.utils import get_metrc

metrc = get_metrc("item")


class Item(Document):
	def validate(self):
		self.create_or_update_item()
		self.check_item()

	def after_rename(self, old, new, merge=False):
		self.create_or_update_item()

	def create_or_update_item(self):
		data = [
			{
				"ItemCategory": self.category,
				"Name": self.name,
				"UnitOfMeasure": self.unit_of_measure,
				"Strain": self.strain,
				"UnitThcContent": self.thc_content,
				"UnitThcContentUnitOfMeasure": self.thc_content_uom,
				"UnitVolume": self.volume,
				"UnitVolumeUnitOfMeasure": self.volume_uom,
				"UnitWeight": self.weight,
				"UnitWeightUnitOfMeasure": self.weight_uom
			}
		]

		if not self.item_id:
			# Create Room in Metrc and assign ID
			response = metrc.post("/items/v1/create", data)
			if response != "Success":
				frappe.throw(response)
		else:
			data[0].update({"Id": self.item_id})
			# use the update API to update the object if room id exists
			response = metrc.post("/items/v1/update", data)
			if response != "Success":
				frappe.throw(response)

	def check_item(self):
		# Try to find if the room id was assigned
		items = metrc.get("/items/v1/active")
		for item in items:
			if item.get("Name") == self.item_name:
				self.item_id = item.get("Id")

	def on_trash(self):
		metrc.delete("/items/v1/" + self.item_id)
