import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def getFundsByFinancialYear(financial_year):
       return {
              "committed": getCommittedFundsByFinancialYear(financial_year),
              "expected" : getExpectedFundsByFinancialYear(financial_year)     
            }
    
def getExpectedFundsByFinancialYear(financial_year):

        sql_query = """
            SELECT IFNULL(round(sum(amount)),0) as Expected_Amount
            FROM `tabFunder`
            WHERE funder_status = 'expected' AND financial_year = %(financial_year)s
        """
        response = frappe.db.sql(sql_query, {"financial_year": financial_year}, as_dict=True)
        return response[0]["Expected_Amount"]
        



def getCommittedFundsByFinancialYear(financial_year):
        sql_query = """
            SELECT IFNULL(round(sum(tranche_amount)),0) as Commited_Amount
            FROM `tabDonation`
            WHERE financial_year = %(financial_year)s
        """
        response = frappe.db.sql(sql_query, {"financial_year": financial_year}, as_dict=True)
        return response[0]["Commited_Amount"]
     