import frappe
from frappe.model.document import Document
from frappe import _

class Utilisation(Document):
    def before_save(self):
        self.validate_utilisation_amount()

    def on_submit(self):
        self.update_overall_utilisation_amount()
        self.update_left_over_donation()

    def validate_utilisation_amount(self):
        overall_donation = self.donor_id
        overall_donation_doc = frappe.get_doc("Overall Donation", overall_donation)
        left_over_donation = overall_donation_doc.available_donation_amount

        if self.utilisation_amount > left_over_donation:
            frappe.throw("Utilisation amount cannot be greater than the available donation amount.")

    def update_overall_utilisation_amount(self):
        overall_donation = self.donor_id
        overall_donation_doc = frappe.get_doc("Overall Donation", overall_donation)
        overall_donation_doc.total_utilisation += self.utilisation_amount
        overall_donation_doc.save()

    def update_left_over_donation(self):
        overall_donation = self.donor_id
        overall_donation_doc = frappe.get_doc("Overall Donation", overall_donation)
        overall_donation_doc.available_donation_amount = overall_donation_doc.total_donation - overall_donation_doc.total_utilisation
        overall_donation_doc.save()
        frappe.msgprint(_("Left Over Donation updated for {0}.").format(overall_donation))
