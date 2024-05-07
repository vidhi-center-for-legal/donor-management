import json
import frappe
from frappe import _
import jwt, datetime, requests



SECRET_KEY="I love secret key"
@frappe.whitelist(allow_guest=True)
def auth_api():
    data = frappe.parse_json(frappe.safe_decode(frappe.request.get_data()))
    username =  data.username
    password =  data.password
    if username == "udhyam" and password == "password123":
        token = generate_token(username)
        return {'token': token}
    else:
        return {'message': 'Invalid credentials'}, 401


# Generate a JWT token for the given user
def generate_token(username):
    payload = {
        'sub': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


# Verify the JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

@frappe.whitelist(allow_guest=True)
def donation_data():
    token = request.headers.get('Token')
    if not token:
        return {'message': 'Token is missing'}, 401

    username = verify_token(token)
    if isinstance(username, str):
        #return jsonify({'User_Name': username}), 401
        return {'message': f'{username}! This is a protected endpoint.'}
