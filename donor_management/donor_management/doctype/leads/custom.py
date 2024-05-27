import frappe
from frappe import _

@frappe.whitelist()
def create_or_update_donor(lead_name, email, name, pan_card):
    if not pan_card:
        frappe.throw(_('PAN Card is mandatory for converting to a Donor'))
    try:
        lead_details = frappe.get_doc('Leads', name)
        lead_name = lead_details.lead_name
        print(email)
        existing_donor = frappe.get_all('Donor', filters={'donor_name': lead_name, 'email': email}, limit=1)
        print(existing_donor)
        if not existing_donor:
            return create_new_donor(lead_details, email)
        else:
            return update_existing_donor(existing_donor[0], lead_details, email)
    except Exception as e:
        frappe.logger().error(f'Error in create_or_update_donor: {str(e)}', exc_info=True)
        return {'status': 'error', 'message': _('Error: {0}').format(str(e))}

def update_existing_donor(existing_donor, lead_details, email):
    try:
        donor = frappe.get_doc("Donor", existing_donor.name)
        update_donor_details(donor, lead_details, email)
        donor.save(ignore_permissions = True)
        return True
    except Exception as e:
        frappe.logger().error(f'Error in updating Donor: {str(e)}', exc_info=True)
        return False

def create_new_donor(lead_details, email):
    try:
        donor = frappe.new_doc("Donor")
        update_donor_details(donor, lead_details, email)
        donor.insert(ignore_permissions=True)
        donor.save()
        return True
    except Exception as e:
        frappe.logger().error(f'Error in creating Donor: {str(e)}', exc_info=True)
        return False


def update_donor_details(donor, lead_details, email):
    donor.donor_name = lead_details.lead_name
    donor.email = email
    donor.gender = lead_details.gender
    donor.dob = lead_details.date_of_birth
    donor.phone = lead_details.phone
    donor.organisation_name = lead_details.organisation_name
    donor.preferred_communication_method = lead_details.preferred_communication_method
    donor.designation = lead_details.designation
    donor.pan_card = lead_details.pan_card
    donor.presentation_given = True
    existing_departments = {d.department_name for d in donor.departments}
    

    for department in lead_details.department:
        if department.department_name not in existing_departments:
            donor.append("departments", {"department_name": department.department_name})
    
    existing_attachments = {(a.name1, a.date, a.agent_uploading, a.attachment) for a in donor.presentation_details}
    
    for attachment in lead_details.get("presentation_details"):
        key = (attachment.name1, attachment.date, attachment.agent_uploading, attachment.attachment)
        if key not in existing_attachments:
            donor.append("presentation_details", {
                "name1": attachment.name1,
                "date": attachment.date,
                "agent_uploading": attachment.agent_uploading,
                "attachment": attachment.attachment
            })


