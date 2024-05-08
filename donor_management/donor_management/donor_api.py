import json
import frappe
from frappe import _
import jwt, re
import datetime
from donor_management.donor_management.api import update_donor_donation_details 



def get_api_settings(field):
    sql_query = "SELECT value FROM `tabSingles`    WHERE doctype = 'Udhyam Website API Setting' AND field IN ('"+field+"')"
    response =  frappe.db.sql(sql_query, as_dict=True)
    return response[0]["value"]
    


@frappe.whitelist(allow_guest=True, methods= ['GET'])
def get_token_api():
    try:
        data = frappe.parse_json(frappe.safe_decode(frappe.request.get_data()))
        username = data.username
        password = data.password
        if username == get_api_settings("username") and password == get_api_settings("password"):
            token = generate_token(username)
            return {'token': token}
        else:
            return {'message': 'Invalid credentials'}, 401
    except ValueError as e:
        return {
            "error": "Missing parameters!"
        }


# Generate a JWT token for the given user default token validity is 10 minutes
def generate_token(username):
    time = int(get_api_settings("token_expiry_time_mins"))
    payload = {
        'sub': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
    }
    return jwt.encode(payload, get_api_settings("secret_key"), algorithm='HS256')


# Verify the JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, get_api_settings("secret_key"), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'


def validate_non_blank_field(data):
    for key, value in data.items():
        if not value or value.strip() == "":
            return {
                "error": f"{key} is mandatory"
            }
    return True


def validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    cleaned_phone = "".join(filter(str.isdigit, phone))
    return len(cleaned_phone) == 10


def validate_date_format(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@frappe.whitelist(allow_guest=True, methods=['POST'])
def send_donation_data():
    if "Token" in frappe.request.headers:
        token = frappe.request.headers['Token']
        response = verify_token(token)
        if response == get_api_settings("username"):
            try:
                data = frappe.parse_json(frappe.safe_decode(frappe.request.get_data()))
                return donation_record_validation(data)
            except ValueError as e:
                return {
                    "error": "Donation record is missing!"
                }
        elif response == "Invalid token":
            return {
                'message': 'Invalid token'
            }
        elif response == "Token has expired":
            return {
                'message': 'Token has expired'
            }
    else:
        return {'message': 'Token is missing'}


def donation_record_validation(data):
    mandatory_fields = ["donor_name", "email", "pan_card", "phone", "donation_amount", "date_of_donation"]

    for field in mandatory_fields:
        if field not in data:
            return f"Error: Missing mandatory field '{field}'"

    if not validate_email(data.email):
        return {
            "error": "invalid email format"
        }
    if not validate_phone(data.phone):
        return {
            "error": "invalid phone number"
        }
    if not validate_date_format(data.date_of_donation):
        return {
            "error": "invalid date format"
        }

    response = validate_non_blank_field(data)
    if isinstance(response, bool):
        return update_donor_donation_details(data) 
    elif isinstance(response, dict):
        return response
