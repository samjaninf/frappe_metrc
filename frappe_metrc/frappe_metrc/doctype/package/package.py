# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe_metrc.utils import get_metrc
import random

metrc = get_metrc("package")

class Package(Document):
	def validate(self):
		self.update_package()

	def update_package(self):
		package = metrc.get("/packages/v1/{}".format(self.label))
		if not package:
			return

		self.id = package.get("Id")
		self.package_type = package.get("PackageType")
		self.source_harvest = package.get("SourceHarvestNames")
		self.quantity = package.get("Quantity")
		self.uom = package.get("UnitOfMeasureName")

		harvest_doc = frappe.new_doc("Harvest")
		rooms = [room.get("name") for room in frappe.get_all("Room")]
		harvest_doc.harvest_name = package.get("SourceHarvestNames")
		harvest_doc.drying_room = random.choice(rooms)
		harvest_doc.plant_count = random.randint(50,80)
		harvest_doc.save()

		frappe.db.commit()