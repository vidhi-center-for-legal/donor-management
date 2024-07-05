/*frappe.ui.form.on("Donation", {
    amount_in_preferred_currency: function(frm) {
        var preferred_currency = frm.doc.preferred_currency;
        var amount_in_preferred_currency = frm.doc.amount_in_preferred_currency;
        var date_of_donation = frm.doc.date_of_donation;

        // Check if date of donation is provided
        if (!date_of_donation) {
            // Throw an error and clear the fields
            frappe.msgprint(__("Date of Donation is required."));
            frm.set_value("preferred_currency", "");
            frm.set_value("amount_in_preferred_currency", "");
            return;
        }

        frappe.call({
            method: 'donor_management.donor_management.doctype.donation.donation.exchange_rate',
            args: {
                preferred_currency: preferred_currency,
                amount_in_preferred_currency: amount_in_preferred_currency,
                date_of_donation: date_of_donation
            },
            callback: function(r) {
                if (r.message) {
                    // Update the exchanged_amount field based on the fetched exchange rate
                    var exchangeRate = r.message[0];
                    var exchange_rate = r.message[1]
                    frm.set_value('tranche_amount', exchangeRate);
                    frm.set_value('exchange_rate', exchange_rate);
                }
            }
        });
    },
});*/