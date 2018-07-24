# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "frappe_metrc"
app_title = "Frappe Metrc"
app_publisher = "Neil Lasrado"
app_description = "A simple Frappe app to interact with Metrc API"
app_icon = "octicon octicon-tools"
app_color = "green"
app_email = "neil@digithinkit.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_metrc/css/frappe_metrc.css"
# app_include_js = "/assets/frappe_metrc/js/frappe_metrc.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_metrc/css/frappe_metrc.css"
# web_include_js = "/assets/frappe_metrc/js/frappe_metrc.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "frappe_metrc.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_metrc.install.before_install"
# after_install = "frappe_metrc.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_metrc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry": {
		"on_submit": ["frappe_metrc.utils.create_package",
                    "frappe_metrc.utils.add_comment_to_batch"],
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_metrc.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_metrc.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_metrc.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_metrc.tasks.weekly"
# 	]
# 	"monthly": [
# 		"frappe_metrc.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "frappe_metrc.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_metrc.event.get_events"
# }

