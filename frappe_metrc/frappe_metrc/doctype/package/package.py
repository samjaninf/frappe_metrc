# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.utils import get_metrc

metrc = get_metrc("plant_batch")

class Package(Document):
	def validate(self):
		self.get_data()

	def get_data(self):
		if not self.id:
			package = metrc.get("/packages/v1/{}".format(self.label))
			if package:
				self.id = package.get("Id")