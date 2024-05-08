import frappe
@frappe.whitelist(allow_guest=True)

def update_donor_donation_details(data):
    try:
        update_donor_details(data)
        return {
            "success": "True"
        }
    except Exception as e:
        frappe.log_error(str(e))
        
        return str(e)

def update_donor_details(data):
    existing_donor = frappe.get_all("Donor", filters={"donor_name": data['donor_name'], "email": data['email']})
    if existing_donor:
        donor = frappe.get_doc("Donor", existing_donor[0].name)
        create_donor_donation(donor, data)
    else:
        donor = frappe.new_doc("Donor")
        create_donor_donation(donor, data)

def create_donor_donation(donor, data):
    donor.donor_name = data.donor_name
    donor.pan_card = data.pan_card
    donor.phone = data.phone
    donor.address = data.address
    donor.email = data.email
    donor.save(ignore_permissions=True)
    create_donation(data, donor)

def create_donation(data, donor):
    print(data)
    print(donor)
    donation = frappe.new_doc("Donation")
    donation.update({
        "doctype": "Donation",
        "donor_id": donor.name,
        "date_of_donation": data['date_of_donation'],
        "tranche_amount": data['donation_amount']
    })

    donation.insert(ignore_permissions=True)

    