from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from core.config import settings
from agent.utils import *

USERNAME = settings.LINKEDIN_USERNAME
PASSWORD = settings.LINKEDIN_PASSWORD
COOKIE_PATH = settings.COOKIE_PATH
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (often recommended for headless)
chrome_options.add_argument("--window-size=1920x1080")  # Set window size to ensure all content is loaded

def is_logged_in(driver) -> bool:
    # Check if the user is logged in by looking for a specific element
    div_body = locate_element(driver=driver, by=By.CLASS_NAME, value='application-outlet')
    if div_body:
        return True
    else:
        return False
    
#region LOGIN ANOTHER ACC
def login_another_account(driver: webdriver.Chrome, username: str = USERNAME, password: str = PASSWORD, cookie_path: str = COOKIE_PATH):
    wait = WebDriverWait(driver,15)
    url = 'https://www.linkedin.com/checkpoint/lg/sign-in-another-account'
    driver.get(url)
    sleep(3)

    email_field = driver.find_element(by=By.ID, value="username")
    email_field.send_keys(username)
    sleep(1)

    password_field = driver.find_element(by=By.NAME, value="session_password")
    password_field.send_keys(password)
    password_field.send_keys
    sleep(1)

    signin_field = driver.find_element(by=By.XPATH, value='//*[@id="organic-div"]/form/div[3]/button')
    signin_field.click()
    sleep(2)
    save_cookies(driver, cookie_path)
#endregion

#region LOGIN CURRENT ACC
def login_current_account(driver: webdriver.Chrome, username: str=USERNAME, password: str=PASSWORD, cookie_path: str = COOKIE_PATH):
    url = 'https://www.linkedin.com/login'
    driver.get(url)

    if os.path.exists(cookie_path):
        # Load cookies
        load_cookies(driver=driver, cookies_file=cookie_path)
        driver.refresh()                

    if not (is_logged_in(driver=driver)):
        login_another_account(driver=driver)
    else:
        sleep(2)
#endregion     

def get_driver() -> webdriver.Chrome: # type: ignore
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    login_current_account(driver=driver)

    return driver