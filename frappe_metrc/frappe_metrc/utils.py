# -*- coding: utf-8 -*-
# Copyright (c) 2018, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import requests
from frappe.model.document import Document
from frappe_metrc.frappe_metrc.metrc.request import METRC

def get_metrc(license_type):
	metrc_settings = frappe.db.get_singles_dict("Metrc API Settings")
	license = metrc_settings.get(license_type)
	return METRC(metrc_settings.api_key,  metrc_settings.user_key, license, url="https://sandbox-api-ca.metrc.com/")
