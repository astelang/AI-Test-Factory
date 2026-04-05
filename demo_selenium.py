from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- CONFIGURATION ---
# Using a real practice site for your demo
URL = "https://the-internet.herokuapp.com/login"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
TIMEOUT = 10 

# --- SETUP BROWSER ---
options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized") # Optional: Opens browser in full screen
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, TIMEOUT)

def login_to_account():
    print(f"🚀 Navigating to: {URL}")
    driver.get(URL)
    
    print("✍️ Entering Credentials...")
    # The AI correctly identified using 'wait' instead of 'sleep'
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    
    print("🖱️ Clicking Login...")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))).click()

def verify_success():
    print("✅ Verifying Login Status...")
    # Check if the success flash message appears
    success_msg = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    if "You logged into a secure area!" in success_msg:
        print("🌟 SUCCESS: AI-Generated Logic Passed!")
    else:
        print("❌ FAILED: Login message not found.")

def close_browser():
    print("🔒 Closing browser in 5 seconds...")
    time.sleep(5) # Keeping it open so you can see the result
    driver.quit()

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        login_to_account()
        verify_success()
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
    finally:
        close_browser()