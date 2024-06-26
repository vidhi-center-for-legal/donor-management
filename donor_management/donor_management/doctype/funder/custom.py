import frappe
from frappe import _

@frappe.whitelist()
def create_or_update_donor(funder_status,naming_series):
    if (funder_status!="Expected"):
        frappe.throw(_('Lead status should be Expected'))
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
    #@Todo update veriables based on Funder Doctype
    donor.donor_name = funder_details.lead_name
    donor.email = "a@g.com"
    donor.gender = funder_details.gender
    donor.dob = funder_details.date_of_birth
    donor.phone = funder_details.phone
    donor.organisation_name = funder_details.organisation_name
    donor.preferred_communication_method = funder_details.preferred_communication_method
    donor.designation = funder_details.designation
    donor.pan_card = funder_details.pan_card
    donor.presentation_given = True
    existing_departments = {d.department_name for d in donor.departments}
    

    for department in funder_details.department:
        if department.department_name not in existing_departments:
            donor.append("departments", {"department_name": department.department_name})
    
    existing_attachments = {(a.name1, a.date, a.agent_uploading, a.attachment) for a in donor.presentation_details}
    
    for attachment in funder_details.get("presentation_details"):
        key = (attachment.name1, attachment.date, attachment.agent_uploading, attachment.attachment)
        if key not in existing_attachments:
            donor.append("presentation_details", {
                "name1": attachment.name1,
                "date": attachment.date,
                "agent_uploading": attachment.agent_uploading,
                "attachment": attachment.attachment
            })
    existing_todo_items = {(t.task, t.status, t.notes) for t in donor.to_do}

    for todo in funder_details.get("to_do"):
        key = (todo.task, todo.status, todo.notes)
        if key not in existing_todo_items:
            donor.append("to_do",{
                "task": todo.task,
                "status": todo.status,
                "notes":todo.notes 
            })


