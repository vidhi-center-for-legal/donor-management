import frappe
from frappe import _


@frappe.whitelist()
def leads_count(agent_id):
    try:
        current_agent_leads_count = frappe.db.count(
            "Leads",
            filters={"agent_handling_the_lead": agent_id}
        )
        
        return {"current_agent_leads_count": current_agent_leads_count}
    
    except Exception as e:
        frappe.log_error(f"Error occurred while counting leads: {str(e)}", "Leads Count Error")
        return {"current_agent_leads_count": 0}


@frappe.whitelist()
def update_leads_for_transferred_agent(agent_name, agent_for_lead_transfer, agent_id):
    try:
        current_agent_leads = frappe.get_all(
            "Leads",  # Ensure "Lead" is the correct DocType name
            filters={"agent_handling_the_lead": agent_id},
            fields=["name"]
        )

        for lead in current_agent_leads:
            frappe.db.set_value("Leads", lead.name, "agent_handling_the_lead", agent_for_lead_transfer)

        return f"Leads updated successfully from {agent_name} to {agent_for_lead_transfer}."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Failed to update leads')
        return f"Error occurred: {str(e)}"





