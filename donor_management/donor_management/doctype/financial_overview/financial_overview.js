frappe.ui.form.on('Financial Overview', {
    after_save: function(frm) {
        
        frappe.call({
            method: "donor_management.donor_management.doctype.financial_overview.financial.getFundsByFinancialYearAndFunderType",
           
            args: {
                
                financial_year: frm.doc.name,
                fund_type: 'committed',
                
            },
            callback: function(data) {
                frm.set_value("total_funds_received",data.message);   
                frm.set_value("fr_targets", frm.doc.budget_amount*.15);
                frm.set_value("total_fr_budget", frm.doc.budget_amount+frm.doc.fr_targets);
                frm.set_value("fr__gap", frm.doc.total_fr_budget-frm.doc.mou_billing_expected);
                frm.set_value("budget_gap", frm.doc.budget_amount-frm.doc.mou_billing_expected);         
            }
        });
        frappe.call({
            method: "donor_management.donor_management.doctype.financial_overview.financial.getFundsByFinancialYearAndFunderType",
           
            args: {
                financial_year: frm.doc.name,
                fund_type: 'expected'
            },
            callback: function(data) {
                frm.set_value("funds_committed_and_expected",data.message+frm.doc.total_funds_received);
            }
        });
        
        frm.set_value("expected_income",frm.doc.total_funds_received+frm.doc.funds_committed_and_expected+frm.doc.mou_billing_expected+frm.doc.mou_billing_raised+frm.doc.interest_income)
        frm.save();

        
    }
});