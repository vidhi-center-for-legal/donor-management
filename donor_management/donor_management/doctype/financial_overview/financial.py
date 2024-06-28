import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def getTotalCommittedFundsByFinancialYear(financial_year):
    sql_query = """
        SELECT round(sum(tranche_amount)) as amount
        FROM `tabDonation`
        WHERE  financial_year = %(financial_year)s
    """
    response = frappe.db.sql(sql_query, {"financial_year": financial_year}, as_dict=True)
    return response[0]["amount"] if response else None



@frappe.whitelist(allow_guest=True)
def getTotalExpectedFundsByFinancialYear(financial_year):
    sql_query = """
        SELECT round(sum(tranche_amount)) as amount
        FROM `tabDonation`
        WHERE  financial_year = %(financial_year)s
    """
    response = frappe.db.sql(sql_query, {"financial_year": financial_year}, as_dict=True)
    return response[0]["amount"] if response else None