import frappe
from frappe import _

@frappe.whitelist()
def get_active_agents(doc, agent_name):
    active_agents = frappe.get_all(
        "Agent",
        filters={"agent_status": "Active"},
        fields=["name", "agent_name"] 
    )
    return {"active_agents": active_agents}

@frappe.whitelist()
def leads_count(agent_name):
    
    current_agent = agent_name

    current_agent_leads_count = frappe.get_value(
        "Leads",
        filters={"agent_handling_the_lead": current_agent},
        fieldname="count(name)"
    )
    print(current_agent_leads_count)
    return {"current_agent_leads_count": current_agent_leads_count}

@frappe.whitelist()
def update_leads_for_transferred_agent(doc, agent_name, agent_for_lead_transfer):
    try:
        current_agent_leads = frappe.get_all(
            "Leads",
            filters={"agent_handling_the_lead": agent_name},
            fields=["name"]
        )
        new_agent_leads = frappe.get_all(
            "Leads",
            filters={"agent_handling_the_lead": agent_for_lead_transfer},
            fields=["name"]
        )

        for lead in current_agent_leads:
            frappe.db.set_value("Leads", lead.name, "agent_handling_the_lead", agent_for_lead_transfer)

        return f"Leads updated successfully from {agent_name} to {agent_for_lead_transfer}."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Failed to update leads')
        return f"Error occurred: {str(e)}"




