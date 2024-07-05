import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    date_range = filters.get("date_range")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    quarter = filters.get("quarter")
    year = filters.get("year")

    columns = [
        {"label": _("Donor ID"), "fieldname": "donor_id", "fieldtype": "Link", "options": "Donor", "width": 150},
        {"label": _("Donor Name"), "fieldname": "donor_name", "fieldtype": "Data", "width": 150},
        {"label": _("Email"), "fieldname": "email", "fieldtype": "Data", "width": 160},
        {"label": _("Latest Donation Date"), "fieldname": "latest_donation_date", "fieldtype": "Date", "width": 150},
        # {"label": _("Donor Type"), "fieldname": "donor_type", "fieldtype": "Data", "width": 150},
        {"label": _("Total Donation Amount"), "fieldname": "total_donation_amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Total Utilisation Amount"), "fieldname": "total_utilisation_amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Available Donation Amount"), "fieldname": "available_donation_amount", "fieldtype": "Currency", "width": 180},
    ]

    data = []
    if from_date and to_date :
        overall_donations = frappe.get_all(
        "Overall Donation",
        filters={"latest_donation_date": ["between", [from_date, to_date]]},
        fields=["donor_id", "donor_name", "latest_donation_date", "total_donation", "total_utilisation", "available_donation_amount", "donor_email"],
    )
         
    else:
        overall_donations = frappe.get_all(
        "Overall Donation",
        filters={},
        fields=["donor_id", "donor_name", "latest_donation_date", "total_donation", "total_utilisation", "available_donation_amount", "donor_email"],
    )
    # Process overall donations data
    for overall_donation in overall_donations:
        data.append({
            "donor_id": overall_donation.donor_id,
            "donor_name": overall_donation.donor_name,
            "email": overall_donation.donor_email,
            "latest_donation_date": overall_donation.latest_donation_date,
            # "donor_type": overall_donation.donor_type,
            "total_donation_amount": overall_donation.total_donation,
            "total_utilisation_amount": overall_donation.total_utilisation,
            "available_donation_amount": overall_donation.available_donation_amount,
        })

    return columns, data
