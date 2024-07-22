import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import __version__ as selenium_version
from webdriver_manager.chrome import ChromeDriverManager

def check_user_existence(phone_number):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Set a default window size

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Print Selenium version
        print(f"Selenium Version: {selenium_version}")
        
        # Print ChromeDriver version
        chrome_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        print(f"ChromeDriver Version: {chrome_version}")

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
        print(f"Error: {e}", file=sys.stderr)
        
        # Capture screenshot
        screenshot_path = os.path.join(os.path.dirname(__file__), f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}", file=sys.stderr)
        
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python selenium_script.py <phone_number>")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    result = check_user_existence(phone_number)
    print(result)