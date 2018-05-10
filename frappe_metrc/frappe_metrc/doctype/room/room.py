# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests

class Room(Document):
	def validate(self):
		metrc_settings = frappe.get_single("Metrc API Settings")
		auth=(metrc_settings.api_key, metrc_settings.user_key)
		params={"licenseNumber": metrc_settings.room}
			
		if not self.room_id:
			#Create Room in Metrc and assign ID
			data=[{
				"Name": self.room_name
			}]
			post_url = metrc_settings.url + "/rooms/v1/create"
			#metrc will return a 200 if all is good
			#it won't send the id of the room; you need to guess that out
			requests.post(url=post_url, auth=auth, params=params, json=data)

			#Try to find if the room id was assigned 
			get_url = metrc_settings.url + "/rooms/v1/active"
			response = requests.get(url=get_url, auth=auth, params=params)
			for room in response.json():
				if room.get("Name") == self.room_name:
					self.room_id = room.get("Id")
		else:
			#use the update API to update the object if room id exists
			data=[{
				"Id": self.room_id,
				"Name": self.room_name
			}]
			post_url = metrc_settings.url + "/rooms/v1/update"
			requests.post(url=post_url, auth=auth, params=params, json=data)

