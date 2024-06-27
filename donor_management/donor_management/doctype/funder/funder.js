function convertToDonor(frm) {
  
    frappe.confirm(
        __('This action will create a new donor record in commited stage with the following details:') +
        '<br><br>' +
        __('Funder Name: {0}', [frm.doc.organisation_name]) ,
        () => { 
            frappe.call({
                method: "donor_management.donor_management.doctype.funder.custom.create_or_update_donor",
                //@Todo: update the api end point
                args: {
                    funder_status: frm.doc.funder_status,
                    naming_series: frm.doc.name,
                },
                callback: function(r) {
                    if (r.message) { 
                        frm.set_value("funder_status", "Committed");
                        frm.save().then(() => {
                            frappe.msgprint(__('Funder converted to donor successfully.'));
                        });
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

frappe.ui.form.on('Funder', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && !frm.doc.donor) {
            frm.add_custom_button(__('Convert to committed stage'), function() {
                if(frm.doc.funder_status=="Pipeline" || frm.doc.funder_status=="Committed")
                    {
                        frappe.msgprint(__('Funder sould be in expected stage for converting it as Donor!'+frm.doc.name));
                        
                    }
                    else{
                        convertToDonor(frm);
                    }
               
            }).addClass('btn-primary');
        }
    }
});
