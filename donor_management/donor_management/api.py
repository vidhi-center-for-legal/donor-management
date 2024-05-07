import frappe
import jwt
import datetime
@frappe.whitelist(allow_guest=True)


def ping():
    try:
        data = get_request_form_data()
        #print(data)
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
    
    donation = frappe.new_doc("Donation", filters = {"donor_name": donor.donor_name})
    donation.donor_id = donor.donor_id
    donation.date_of_donation = data.date_of_donation
    donation.tranche_amount = data.donation_amount
    
    donation.save(ignore_permissions = True)
    
    
def get_request_form_data():
	if frappe.form_dict.data is None:
		data = frappe.safe_decode(frappe.request.get_data())
	else:
		data = frappe.form_dict.data

	try:
		return frappe.parse_json(data)
	except ValueError:
		return frappe.form_dict