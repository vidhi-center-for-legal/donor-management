import frappe
from frappe.model.document import Document
from erpnext.setup.utils import get_exchange_rate

class Donation(Document):
    def on_submit(self):
        add_donation_to_test(self)
        left_over_donation_amount(self)

def left_over_donation_amount(doc):
    donation_amount = doc.tranche_amount
    frappe.db.set_value("Donation", doc.name, "left_over_donation", donation_amount)


@frappe.whitelist()
def exchange_rate(preferred_currency, amount_in_preferred_currency, date_of_donation):
    try:
        amount = float(amount_in_preferred_currency)
        exchange_rate = get_exchange_rate(preferred_currency, 'INR', date_of_donation)
        exchanged_amount = amount * exchange_rate
        return exchanged_amount, exchange_rate

    except Exception as e:
        frappe.logger().error(f"Error in exchange_rate: {str(e)}", exc_info=True)
        return {"status": "error", "message": f"Error: {str(e)}"}
    
@frappe.whitelist()
def add_donation_to_test(doc):
    try:
        donation_details = frappe.get_doc(doc)
        donor_id = donation_details.get("donor_id")

        overall_donation_document = frappe.get_all('Overall Donation', filters={'donor_id': donor_id}, limit=1)

        if not overall_donation_document:
            add_new_overall_donation(donation_details)
        else:
            update_overall_donation(donation_details)
    except frappe.DoesNotExistError:
        add_new_overall_donation(donation_details)
    except Exception as e:
        frappe.log_error(f"Error in add_donation_to_test: {e}", "Donation Processing")

def add_new_overall_donation(doc):
    try:
        new_overall_donation_document = frappe.new_doc("Overall Donation")
        new_overall_donation_document.donor_id = doc.get("donor_id")
        new_overall_donation_document.donor_name = doc.get("donor_name")
        new_overall_donation_document.total_donation= doc.get("tranche_amount")
        new_overall_donation_document.available_donation_amount = doc.get("tranche_amount")
        new_overall_donation_document.latest_donation_date = doc.get("date_of_donation")
        new_overall_donation_document.insert(ignore_permissions=True)
        frappe.msgprint("New Overall Donation document created successfully.")
    except Exception as e:
        frappe.log_error(f"Error in add_new_overall_donation: {e}", "Donation Processing")

def update_overall_donation(doc):
    try:
        overall_donation_document = frappe.get_doc("Overall Donation", {"donor_id": doc.get("donor_id")})
        overall_donation_document.total_donation += doc.get("tranche_amount")
        overall_donation_document.available_donation_amount += doc.get("tranche_amount")
        overall_donation_document.latest_donation_date = doc.get("date_of_donation")
        overall_donation_document.save()
        frappe.msgprint("Overall Donation document updated successfully.")
    except Exception as e:
        frappe.log_error(f"Error in update_overall_donation: {e}", "Donation Processing")



