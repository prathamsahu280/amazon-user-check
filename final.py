from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import __version__ as selenium_version

app = Flask(__name__)

def check_user_existence(phone_number):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        input_field.send_keys(phone_number)
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "auth-password-missing-alert"))
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        driver.quit()

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