# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document

def get_metrc_config():
	metrc_settings = frappe.db.get_singles_dict("Metrc API Settings")

	base_url = metrc_settings.url
	auth = (metrc_settings.api_key, metrc_settings.user_key)
	params = {"licenseNumber": metrc_settings.lab_test}

	return base_url, auth, params
