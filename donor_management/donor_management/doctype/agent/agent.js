frappe.ui.form.on('Agent', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('Transfer Leads'), function() {
                transferLeads(frm);
            }).addClass('btn-danger');
        }
    }
});

function transferLeads(frm) {
    var agent_name = frm.doc.agent_name;

    frappe.call({
        method: 'donor_management.donor_management.doctype.agent.custom.leads_count',
        args: {
            agent_name: agent_name
        },
        callback: function(r) {
            if (r.message) {
                var totalLeads = r.message.current_agent_leads_count;
                var message = `Total Leads: ${totalLeads}`;
                if (totalLeads > 0) {
                    frappe.prompt([
                        {
                            label: message + '\n\nSelect Agent',
                            fieldname: 'agent_for_lead_transfer',
                            fieldtype: 'Link',
                            options: 'Agent',
                            reqd: 1,
                            get_query: function() {
                                return {
                                    filters: {
                                        agent_status: 'Active',
                                        name: ['not in', [frm.doc.name]]
                                    }
                                };
                            }
                        }
                    ],
                    function(values) {
                        if (values) {
                            

                            frappe.confirm(
                                __('Are you sure you want to transfer the leads?'),
                                () => {
                                        updateLeads(frm);
                                        frm.set_value('agent_for_lead_transfer', values.agent_for_lead_transfer);
                                        frm.set_value('agent_status', 'Left')
                                    },
                                    () => {
                                        frappe.msgprint('Lead transfer canceled.');
                                    }
                                
                            );
                        }
                    },
                    'Select Agent'
                    );
                }
             else {
                frappe.msgprint('No Leads to Transfer');
                
                
            }
        }
    }
    });
}

function updateLeads(frm) {
    var agent_for_lead_transfer = frm.doc.agent_for_lead_transfer;
    var agent_name = frm.doc.agent_name;

    frappe.call({
        method: 'donor_management.donor_management.doctype.agent.custom.update_leads_for_transferred_agent',
        args: {
            doc: frm.doc,
            agent_for_lead_transfer: agent_for_lead_transfer,
            agent_name: agent_name
        },
        callback: function(r) {
            if (r.message) {
                frappe.msgprint(r.message);
                frm.save();
            } else {
                frappe.msgprint('Failed to update leads.');
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            frappe.msgprint('Error occurred while updating leads.');
        }
    });
}
