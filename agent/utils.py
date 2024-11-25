from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from time import sleep
import pickle

def locate_element(driver: webdriver.Chrome, by: str, value: str) -> WebElement:
    sleep(0.5)
    try:
        element = driver.find_element(by,value)
        return element
    except NoSuchElementException:
        return None
    
def save_cookies(driver: webdriver.Chrome, cookies_file: str):
    with open(cookies_file, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver: webdriver.Chrome, cookies_file: str):
    with open(cookies_file, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def get_fullxpath(driver: webdriver.Chrome, element: WebElement) -> str:
    return driver.execute_script( 
     '''function getElementXPath(elt) {
            var path = "";
            for (; elt && elt.nodeType == 1; elt = elt.parentNode) {
                idx = getElementIdx(elt);
                xname = elt.tagName;
                if (idx > 1) xname += "[" + idx + "]";
                path = "/" + xname + path;
            }
            return path;
        }

        function getElementIdx(elt) {
            var count = 1;
            for (var sib = elt.previousSibling; sib; sib = sib.previousSibling) {
                if (sib.nodeType == 1 && sib.tagName == elt.tagName) count++;
            }
            return count;
        }

        return getElementXPath(arguments[0]);''',
        element
    ).lower()

def is_bottom_of_page(driver: webdriver.Chrome) -> bool:
    # Get the current scroll position and the total scrollable height
    current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
    total_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    return current_scroll_position >= total_scroll_height