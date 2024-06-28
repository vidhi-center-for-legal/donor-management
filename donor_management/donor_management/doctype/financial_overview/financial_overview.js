frappe.ui.form.on('Financial Overview', {
    refresh: function(frm) {
        frm.set_value("fr_targets", frm.doc.budget_amount*.15);
        frm.set_value("total_fr_budget", frm.doc.budget_amount+frm.doc.fr_targets);
        frm.set_value("fr__gap", frm.doc.total_fr_budget-frm.doc.mou_billing_expected);
        frm.set_value("budget_gap", frm.doc.budget_amount-frm.doc.mou_billing_expected);
        frappe.call({
            method: "donor_management.donor_management.doctype.financial_overview.financial.getTotalDonatiosByFinancialYear",
           
            args: {
                financial_year: frm.doc.name,
            },
            callback: function(data) {
                frm.set_value("total_funds_received",data.message);
                frm.save();
                
            }
        });


        
    }
});