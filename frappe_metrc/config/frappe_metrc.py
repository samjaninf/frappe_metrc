# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Cultivation"),
            "icon": "fa fa-leaf",
            "items": [
                {
                    "type": "doctype",
                    "name": "Plant",
                },
                {
                    "type": "doctype",
                    "name": "Plant Batch",
                },
                {
                    "type": "doctype",
                    "name": "Strain",
                },
                {
                    "type": "doctype",
                    "name": "Room",
                },
                {
                    "type": "doctype",
                    "name": "Harvest",
                },
                # {
                #     "type": "doctype",
                #     "name": "Lab Test",
                # },
            ]
        },
        {
            "label": _("Inventory"),
            "icon": "fa fa-leaf",
            "items": [
                {
                    "type": "doctype",
                    "name": "Package",
                },
                {
                    "type": "doctype",
                    "name": "Transfer",
                },
            ]
        },
        {
            "label": _("Setup"),
            "icon": "fa fa-leaf",
            "items": [
                {
                    "type": "doctype",
                    "name": "Metrc API Settings",
                    "label": "METRC Settings"
                },
                {
                    "type": "doctype",
                    "name": "BioTrackTHC API Settings",
                    "label": "BioTrackTHC Settings"
                },
                {
                    "type": "doctype",
                    "name": "MJ Freeway API Settings",
                    "label": "MJ Freeway Settings"
                },
            ]
        },
        {
            "label": _("Logs"),
            "icon": "fa fa-leaf",
            "items": [
                {
                    "type": "doctype",
                    "name": "API Request Log",
                    "label": "API Request Log"
                },
            ]
        },
    ]
