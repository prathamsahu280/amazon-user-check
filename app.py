import os
import logging
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set environment variables directly in the script
os.environ['GOOGLE_CHROME_BIN'] = '/usr/bin/google-chrome'
os.environ['CHROMEDRIVER_PATH'] = '/usr/local/bin/chromedriver'

def check_user_existence(phone_number):
    logger.info(f"Checking user existence for phone number: {phone_number}")
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    logger.debug(f"Chrome binary location: {chrome_options.binary_location}")
    logger.debug(f"ChromeDriver path: {os.environ.get('CHROMEDRIVER_PATH')}")

    try:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        logger.info("WebDriver initialized successfully")
        
        driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        logger.info("Navigated to Amazon sign-in page")
        
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        input_field.send_keys(phone_number)
        logger.info("Entered phone number")
        
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()
        logger.info("Clicked continue button")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "auth-password-missing-alert"))
        )
        logger.info("User exists")
        return True
    except Exception as e:
        logger.error(f"Error in check_user_existence: {str(e)}")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info("WebDriver quit")

@app.route('/check_user', methods=['POST'])
def check_user():
    logger.info("Received request to /check_user")
    data = request.json
    phone_number = data.get('phone_number')
    
    if not phone_number:
        logger.warning("Phone number not provided")
        return jsonify({"error": "Phone number is required"}), 400
    
    user_exists = check_user_existence(phone_number)
    logger.info(f"User exists: {user_exists}")
    return jsonify({"user_exists": user_exists})

@app.route('/')
def home():
    logger.info("Home route accessed")
    return "App is running"

if __name__ == '__main__':
    logger.info("Starting Flask application")
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)