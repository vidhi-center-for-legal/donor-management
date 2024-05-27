import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    donor_id = filters.get("donor")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    project = filters.get("project_details")
    
    if not from_date:
        from_date = frappe.utils.add_days(frappe.utils.today(), -365)
    if not to_date:
        to_date = frappe.utils.today()
    
    columns = get_columns()
    donations = get_donations(donor_id, from_date, to_date, project)
    data = format_donation_data(donations)
    
    return columns, data

def get_donations(donor_id=None, from_date=None, to_date=None, project=None):
    filters = {
        "docstatus": 1,
        "date_of_donation": ["between", [from_date, to_date]]
    }
    if donor_id:
        filters["donor_id"] = donor_id
    if project:
        filters["project"] = project

    donations = frappe.get_all(
        "Donation",
        filters=filters,
        fields=["donor_id", "donor_name", "date_of_donation", "tranche_amount", "project"],
    )
    
    return donations

def format_donation_data(donations):
    data = []
    for donation in donations:
        data.append({
            "donor_id": donation.donor_id,
            "donor_name": donation.donor_name,
            "date_of_donation": donation.date_of_donation,
            "tranche_amount": donation.tranche_amount,
            "project": donation.project
        })
    return data

def get_columns():
    return [
        {"label": _("Donor ID"), "fieldname": "donor_id", "fieldtype": "Link", "options": "Donor", "width": 180},
        {"label": _("Donor Name"), "fieldname": "donor_name", "fieldtype": "Data", "width": 180},
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options":"Project Details","width": 180},
        {"label": _("Date of Donation"), "fieldname": "date_of_donation", "fieldtype": "Date", "width": 150},
        {"label": _("Donation Amount"), "fieldname": "tranche_amount", "fieldtype": "Currency", "width": 180},
    ]
