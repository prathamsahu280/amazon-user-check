import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def check_user_existence(phone_number):
    url = "https://www.amazon.in/ap/signin"
    params = {
        "openid.pape.max_auth_age": "0",
        "openid.return_to": "https://www.amazon.in/?ref_=nav_signin",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.assoc_handle": "inflex",
        "openid.mode": "checkid_setup",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.ns": "http://specs.openid.net/auth/2.0"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    session = requests.Session()
    response = session.get(url, params=params, headers=headers)
    
    # Get the form action URL
    form_action = response.text.split('action="')[1].split('"')[0]
    
    # Prepare the form data
    form_data = {
        "email": phone_number,
        "create": "0",
        "password": ""
    }
    
    # Submit the form
    response = session.post(form_action, data=form_data, headers=headers)
    
    # Check if the response contains the password field
    return "password" in response.text

@app.route('/api/check_user', methods=['POST'])
def api_check_user():
    phone_number = request.json.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    result = check_user_existence(phone_number)
    return jsonify({"exists": result})

@app.route('/')
def home():
    return "Welcome to the Amazon User Checker API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)