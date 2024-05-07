# Copyright (c) 2024, Tech4Good Community and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Donor ID"), "fieldname": "donor_id", "fieldtype": "Link", "options": "Donor", "width": 180},
        {"label": _("Donor Name"), "fieldname": "donor_name", "fieldtype": "Data", "width": 180},
        {"label": _("Utilisation Amount"), "fieldname": "utilisation_amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Utilisation Date"), "fieldname": "utilisation_date", "fieldtype": "Date", "width": 130},
        {"label": _("Utilisation Type"), "fieldname": "utilisation_type", "fieldtype": "Data", "width": 180},
        {"label": _("Approved Date"), "fieldname": "approved_date", "fieldtype": "Date", "width": 130}
    ]

def get_data(filters):
    utilisation_filters = {"docstatus": 1}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    if from_date and to_date:
        utilisation_filters["date_of_utilisation"] = ["between", [from_date, to_date]]

    # Check if donor_name filter is specified
    donor_name = filters.get("donor_name")
    if donor_name:
        utilisation_filters["donor_id"] = donor_name
        
    utilisation_type = filters.get("utilisation_type")
    if utilisation_type:
        utilisation_filters["utilisation_type"] = utilisation_type

    utilisations = frappe.get_all(
        "Utilisation",
        filters=utilisation_filters,
        fields=["name","donor_id", "date_of_utilisation", "donor_name", "utilisation_amount", "approved_date", "utilisation_type"]
    )

    data = []
    for utilisation in utilisations:
        data.append({
            "donor_id": utilisation.donor_id,
            "donor_name": utilisation.donor_name,
            "utilisation_amount": utilisation.utilisation_amount,
            "utilisation_date": utilisation.date_of_utilisation,
            "utilisation_type": utilisation.utilisation_type,
            "approved_date": utilisation.approved_date
        })

    return data
