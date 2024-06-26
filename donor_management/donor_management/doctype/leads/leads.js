function convertToDonor(frm) {
    
    var leadName = frm.doc.lead_name;
    var email = frm.doc.email;
    var lead_status = frm.doc.lead_status;
    


    frappe.confirm(
        __('This action will create a new donor record with the following details:') +
        '<br><br>' +
        __('Funder Name: {0}', [leadName]) +
        '<br>' +
        __('Email: {0}', [email]), // Add email here
        () => { 
            frappe.call({
                method: "donor_management.donor_management.doctype.leads.custom.create_or_update_donor",
                args: {
                    lead_status: lead_status,
                    lead_name: leadName,
                    email: email, 
                    name: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) { 
                        frm.set_value("lead_status", "Committed");
                        frm.save();
                        frappe.msgprint(__('Funder converted to committed stage successfully.'));
                    } else {
                        frappe.msgprint(__('Funder conversion to committed stage failed.'));
                    }
                }
            });
        },
        () => {
            frappe.msgprint(__('Conversion to committed stage cancelled.'));
        }
    );
}

frappe.ui.form.on('Leads', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && !frm.doc.donor) {
            frm.add_custom_button(__('Convert to committed stage'), function() {
                convertToDonor(frm);
            }).addClass('btn-primary');
        }
    }
});
