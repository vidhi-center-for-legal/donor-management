import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    

    columns = [
        {"label": _("Organisation Name"), "fieldname": "organisation_name", "fieldtype": "Data", "width": 150},
        {"label": _("Email"), "fieldname": "email", "fieldtype": "Data", "width": 160},
        {"label": _("Financial Year"), "fieldname": "financial_year", "fieldtype": "Link", "options": "Financial Year", "width": 150},
        {"label": _("Funder Status"), "fieldname": "funder_status", "fieldtype": "Select", "width": 150},
        {"label": _("Funder Type"), "fieldname": "funder_type", "fieldtype": "Link", "options": "Funder Type", "width": 150},
        #{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Total Expected Amount"), "fieldname": "total_expected_amount", "fieldtype": "Currency", "width": 180},
    ]

    data = []

    filters_dict = {
        "funder_status": "Expected"
    }

    # if from_date and to_date:
    #     filters_dict["latest_donation_date"] = ["between", [from_date, to_date]]

    expected_donations = frappe.get_all(
        "Funder",
        filters=filters_dict,
        fields=["organisation_name", "financial_year", "amount", "funder_status", "funder_type", "email"],
    )

    total_expected_amount = 0

    for expected_donation in expected_donations:
        total_expected_amount += expected_donation.amount
        data.append({
            "organisation_name": expected_donation.organisation_name,
            "email": expected_donation.email,
            "financial_year": expected_donation.financial_year,
            "amount": expected_donation.amount,
            "funder_status": expected_donation.funder_status,
            "funder_type": expected_donation.funder_type,
            "total_expected_amount": total_expected_amount,
        })

    return columns, data
