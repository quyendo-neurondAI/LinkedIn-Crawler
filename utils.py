from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

def is_bottom_of_page(driver: webdriver.Chrome) -> bool:
    # Get the current scroll position and the total scrollable height
    current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
    total_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    return current_scroll_position >= total_scroll_height

def infinite_scroll(driver: webdriver.Chrome):
    while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            
            check_showmore = False
            try:
                element = driver.find_element(By.CLASS_NAME, value='''artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button''')
                check_showmore = True

            except NoSuchElementException as e:
                check_showmore = False
                pass

            if check_showmore:
                driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')
                sleep(2)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            if is_bottom_of_page(driver):
                print("Reached the bottom of the page.")
                break

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

def get_urls(driver):
    page_source = BeautifulSoup(driver.page_source)
    profiles = page_source.find_all('a', class_ = 'ember-view mn-connection-card__link')
    all_profile_URL = []
    for profile in profiles:
        profile_ID = profile.get('href')
        profile_URL = "https://www.linkedin.com" + profile_ID
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL