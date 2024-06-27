frappe.query_reports["Overall Donation Expected Report"] = {
    "filters": [

        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "quarter",
            "label": __("Quarter"),
            "fieldtype": "Select",
            "options": "1\n2\n3\n4",
            "default": "1",
            "depends_on": "eval: doc.date_range === 'Quarterly'"
        },
        {
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "default": frappe.defaults.get_user_default("fiscal_year"),
            "depends_on": "eval: doc.date_range === 'Yearly'"
        }
    ]
};

