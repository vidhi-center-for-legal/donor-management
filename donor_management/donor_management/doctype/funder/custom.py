import frappe
from frappe import _

@frappe.whitelist()
def create_or_update_donor(funder_status,naming_series):
    if (funder_status == "Committed"):
        frappe.throw(_('Funder is already in committed stage'))
    elif (funder_status!="Expected"):
        frappe.throw(_('Funder status should be Expected'))
    try:
        funder_details = frappe.get_doc('Funder', naming_series)        
        #lead_name = lead_details.organisation_name
        existing_donor = frappe.get_all('Donor', filters={'donor_name': naming_series,}, limit=1)
        if not existing_donor:
            return create_new_donor(funder_details)
        else:
            return update_existing_donor(existing_donor[0], funder_details)
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

def create_new_donor(funder_details):
    try:
        donor = frappe.new_doc("Donor")
        #@ToDo change the function name as per it work 
        update_donor_details(donor, funder_details)
        donor.insert(ignore_permissions=True)
        donor.save()
        return True
    except Exception as e:
        frappe.logger().error(f'Error in creating Donor: {str(e)}', exc_info=True)
        return False


def update_donor_details(donor, funder_details):
    donor.organisation_name = funder_details.organisation_name
    donor.email = funder_details.email
    donor.website=funder_details.website
    donor.phone = funder_details.phone
    donor.preferred_communication = funder_details.preferred_communication
    donor.assigned_poc_from_vidhi_centre = funder_details.assigned_poc_from_vidhi_centre
    donor.funder_program = funder_details.funder_program
    donor.amount = funder_details.amount
    donor.financial_year = funder_details.financial_year
    donor.funder_type = funder_details.funder_type
    donor.status = funder_details.status
    donor.start_date = funder_details.start_date
    donor.end_date = funder_details.end_date
    donor.presentation_given = True
    existing_departments = {d.department_name for d in donor.departments}
    

    for department in funder_details.department:
        if department.department_name not in existing_departments:
            donor.append("departments", {"department_name": department.department_name})
    
    existing_attachments = {(a.name1, a.date, a.agent_uploading, a.attachment) for a in donor.presentation_details}
    
    for attachment in funder_details.get("presentation_details"):
        key = (attachment.name1, attachment.date, attachment.attachment)
        if key not in existing_attachments:
            donor.append("presentation_details", {
                "name1": attachment.name1,
                "date": attachment.date,
                "attachment": attachment.attachment
            })



