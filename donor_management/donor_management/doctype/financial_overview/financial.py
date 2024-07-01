import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)

def getFundsByFinancialYearAndFunderType(financial_year,fund_type):
    if fund_type == 'committed':
        sql_query = """
            SELECT round(sum(tranche_amount)) as amount
            FROM `tabDonation`
            WHERE financial_year = %(financial_year)s
        """
        response_key = "amount"
    elif fund_type == 'expected':
        sql_query = """
            SELECT round(sum(amount)) as ExpectedAmount
            FROM `tabFunder`
            WHERE funder_status = 'expected' AND financial_year = %(financial_year)s
        """
        response_key = "ExpectedAmount"
    else:
        return None

    response = frappe.db.sql(sql_query, {"financial_year": financial_year}, as_dict=True)
    return response[0][response_key] if response else None
