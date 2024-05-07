function convertToDonor(frm) {
    var leadName = frm.doc.lead_name;
    var email = frm.doc.email;

    frappe.confirm(
        __('This action will create a new donor record with the following details:') +
        '<br><br>' +
        __('Lead Name: {0}', [leadName]) +
        '<br>' +
        __('Email: {0}', [email]), // Add email here
        () => { 
            frappe.call({
                method: "donor_management.donor_management.doctype.leads.custom.create_or_update_donor",
                args: {
                    lead_name: leadName,
                    email: email, // Pass email to Python function
                    name: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) { 
                        frm.set_value("lead_status", "Converted to donor");
                        frm.save();
                        frappe.msgprint(__('Lead converted to donor successfully.'));
                    } else {
                        frappe.msgprint(__('Conversion to donor failed.'));
                    }
                }
            });
        },
        () => {
            frappe.msgprint(__('Conversion to donor cancelled.'));
        }
    );
    
}

frappe.ui.form.on('Leads', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && !frm.doc.donor) {
            frm.add_custom_button(__('Convert to Donor'), function() {
                convertToDonor(frm);
            }).addClass('btn-primary');
        }
    }
});
