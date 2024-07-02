function convertToDonor(frm) {
    const org_name = frm.doc.organisation_name.toUpperCase();
    frappe.confirm(
        __('Click <strong>Yes</strong> button to covert <strong>'+org_name+'</strong> as donor and set funder status as <strong>committed</strong>') ,
        () => { 
            frappe.call({
                method: "donor_management.donor_management.doctype.funder.custom.create_or_update_donor",
                
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
        if (!frm.doc.__islocal && !frm.doc.donor && frm.doc.funder_status!="Committed") {
            frm.add_custom_button(__('Convert to committed funder'), function() {
                
                if(frm.doc.email!=null){
                    if(frm.doc.funder_status=="Pipeline")
                        {
                            frappe.msgprint(__('Funder sould be in expected status for converting it as Donor!'));
                            
                        }
                        else{
                            frm.save();

                            convertToDonor(frm);
                        }
                }
                else{
                    frappe.msgprint(__('Please add Funder email to convert to committed stage.'));
                }
                
               
            }).addClass('btn-primary');
        }
    }
});
