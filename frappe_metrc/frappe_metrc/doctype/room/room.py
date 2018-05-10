# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document


class Room(Document):
	def validate(self):
		base_url, auth, params = get_config()

		if not self.room_id:
			# Create Room in Metrc and assign ID
			data = [{
				"Name": self.room_name
			}]

			create_room_url = base_url + "/rooms/v1/create"

			# metrc will return a 200 if all is good
			# it won't send the id of the room; you need to guess that out
			requests.post(url=create_room_url, auth=auth, params=params, json=data)

			# Try to find if the room id was assigned
			check_room_url = base_url + "/rooms/v1/active"
			response = requests.get(url=check_room_url, auth=auth, params=params)

			for room in response.json():
				if room.get("Name") == self.room_name:
					self.room_id = room.get("Id")
		else:
			# use the update API to update the object if room id exists
			data = [{
				"Id": self.room_id,
				"Name": self.room_name
			}]

			update_room_url = base_url + "/rooms/v1/update"
			requests.post(url=update_room_url, auth=auth, params=params, json=data)

	def on_trash(self):
		base_url, auth, params = get_config()

		delete_room_url = base_url + "/rooms/v1/" + self.room_id
		requests.delete(url=delete_room_url, auth=auth, params=params)


def get_config():
	metrc_settings = frappe.get_single("Metrc API Settings")

	base_url = metrc_settings.url
	auth = (metrc_settings.api_key, metrc_settings.user_key)
	params = {"licenseNumber": metrc_settings.room}

	return base_url, auth, params
