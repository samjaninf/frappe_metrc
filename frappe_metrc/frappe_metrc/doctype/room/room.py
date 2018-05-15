# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.utils import get_metrc_config

class Room(Document):
	BASE_URL, AUTH, PARAMS = get_metrc_config()

	def validate(self):
		self.create_or_update_room()
		self.check_room()

	def create_or_update_room(self):
		data = [
			{
				"Name": self.room_name
			}
		]

		if not self.room_id:
			# Create Room in Metrc and assign ID
			url = BASE_URL + "/rooms/v1/create"
		else:
			# use the update API to update the object if room id exists
			data[0].update({"Id": self.room_id})

			url = BASE_URL + "/rooms/v1/update"

		# metrc will return a 200 if all is good
		# it won't send the id of the room; you need to guess that out
		requests.post(url=url, auth=AUTH, params=PARAMS, json=data)

	def check_room(self):
		# Try to find if the room id was assigned
		url = BASE_URL + "/rooms/v1/active"
		response = requests.get(url=url, auth=AUTH, params=PARAMS)

		for room in response.json():
			if room.get("Name") == self.room_name:
				self.room_id = room.get("Id")

	def on_trash(self):
		delete_room_url = BASE_URL + "/rooms/v1/" + self.room_id
		requests.delete(url=delete_room_url, auth=AUTH, params=PARAMS)

