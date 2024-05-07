import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    donor_id = filters.get("donor")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    if not from_date:
        from_date = frappe.utils.add_days(frappe.utils.today(), -365) 
    if not to_date:
        to_date = frappe.utils.today()
    
    columns = get_columns()
    if donor_id:
        data = get_data_for_donor_id(donor_id, from_date, to_date)
    else:
        data = get_all_donations(from_date, to_date)
    
    return columns, data

def get_data_for_donor_id(donor_id, from_date, to_date):
    data = []
    donations = frappe.get_all(
        "Donation",
        filters={"docstatus": 1, "donor_id": donor_id, "date_of_donation": ["between", [from_date, to_date]]},
        fields=["name", "tranche_amount", "date_of_donation", "donor_name"],
    )
    
    for donation in donations:
        data.append({
            "donor_id": donor_id,
            "donor_name": donation.donor_name,
            "date_of_donation": donation.date_of_donation,
            "tranche_amount": donation.tranche_amount,
        })
    
    return data

def get_all_donations(from_date, to_date):
    data = []
    donations = frappe.get_all(
        "Donation",
        filters={"docstatus": 1, "date_of_donation": ["between", [from_date, to_date]]},
        fields=["donor_id", "donor_name", "date_of_donation", "tranche_amount"],
    )
    
    for donation in donations:
        data.append({
            "donor_id": donation.donor_id,
            "donor_name": donation.donor_name,
            "date_of_donation": donation.date_of_donation,
            "tranche_amount": donation.tranche_amount,
        })
    
    return data

def get_columns():
    return [
        {"label": _("Donor ID"), "fieldname": "donor_id", "fieldtype": "Link", "options": "Donor", "width": 180},
        {"label": _("Donor Name"), "fieldname": "donor_name", "fieldtype": "Data", "width": 180},
        {"label": _("Date of Donation"), "fieldname": "date_of_donation", "fieldtype": "Date", "width": 150},
        {"label": _("Donation Amount"), "fieldname": "tranche_amount", "fieldtype": "Currency", "width": 180},
    ]
