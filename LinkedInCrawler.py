from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from time import sleep

from utils import infinite_scroll, get_fullxpath, is_bottom_of_page, get_urls


class LinkedInCrawler:
    driver: webdriver.Chrome

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    #region LOGIN LINKEDIN
    def login_linkedin(self, username, password):
        sleep(1.5)
        url = 'https://www.linkedin.com/checkpoint/lg/sign-in-another-account'
        self.driver.get(url)
        print('- Finish initializing a self.driver')
        sleep(1.5)

        password = "prodn123"
        username = "skytdv123@gmail.com"
        print('- Finish importing the login credentials')
        sleep(1.5)

        email_field = self.driver.find_element(by=By.ID, value="username")
        email_field.send_keys(username)
        print('- Finish keying in email')
        sleep(1.5)

        password_field = self.driver.find_element(by=By.NAME, value="session_password")
        password_field.send_keys(password)
        password_field.send_keys
        print('- Finish keying in password')
        sleep(1.5)

        signin_field = self.driver.find_element(by=By.XPATH, value='//*[@id="organic-div"]/form/div[3]/button')
        signin_field.click()
        print('- Finish Task: Login to Linkedin')
        sleep(2)
    #endregion


    #region GET CONNECTIONS URLs
    def get_connection_urls(self) -> list:
        sleep(1)
        my_network_btn = self.driver.find_element(By.XPATH, value='//*[@id="global-nav"]/div/nav/ul/li[2]/a')
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(my_network_btn))
        my_network_btn.click()

        sleep(1)
        connections_btn = self.driver.find_element(By.XPATH, value='//*[@id="root"]/div[3]/div[2]/div/div/div/section/div/div/section[1]/div/nav/ul/li[1]/a')
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(connections_btn))
        connections_btn.click()

        #scroll loop
        while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
                
                check_showmore = False
                try:
                    element = self.driver.find_element(By.CLASS_NAME, value='''artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button''')
                    check_showmore = True

                except NoSuchElementException as e:
                    check_showmore = False
                    pass

                if check_showmore:
                    self.driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

                if is_bottom_of_page(self.driver):
                    print("Reached the bottom of the page.")
                    break


        urls = get_urls(self.driver)
        return urls
    #endregion


    #region GET CONTACT INFO
    def get_contact_info(self):
        try:
            sleep(1)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')     
            sleep(0.5)   
            self.driver.execute_script('window.scrollTo(document.body.scrollHeight,0);')
            sleep(0.5)
            a_contact_info = self.driver.find_element(By.ID, value='''top-card-text-details-contact-info''')
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(a_contact_info))
            a_contact_info.click()

            sleep(1.5)
            div_profile_section = self.driver.find_element(By.XPATH, value='''/html/body/div[4]/div/div''')
            div_profile_section_source = BeautifulSoup(div_profile_section.get_attribute('outerHTML'),'html.parser')
            h1_tags = div_profile_section_source.find_all('h1')
            h1_text = [tag.text.strip() for tag in h1_tags]
            h3_tags = div_profile_section_source.find_all('h3')
            h3_text = [tag.text.strip() for tag in h3_tags]
            a_tags = div_profile_section_source.find_all('a')
            a_text = [tag.text.strip() for tag in a_tags]
            span_tags = div_profile_section_source.find_all('span')
            span_text = [tag.text.strip() for tag in span_tags]
            
            exit_btn = self.driver.find_element(By.XPATH, value='''/html/body/div[4]/div/div/button''')
            exit_btn.click()

            return {
                'h1_tag_text': h1_text,
                'h3_tag_text': h3_text,
                'a_tag_text': a_text,
                'span_tang_text': span_text
            }
        except NoSuchElementException as e:
            print(e)    
    #endregion


    #region GET AVAILABLE SECTIONS ON A PROFILE
    def get_sections(self) -> dict:
        sleep(1)
        section_head = {}
        main_element = self.driver.find_element(By.CLASS_NAME, value='scaffold-layout__main')
        main_element_source = BeautifulSoup(main_element.get_attribute('outerHTML'),'html.parser')
        sections = main_element_source.find_all('section', class_='artdeco-card pv-profile-card break-words mt2')
        for i in range(0,len(sections)):
            if len([tag.text.strip() for tag in sections[i].select('span.visually-hidden')]) > 0:
                head = ([tag.text.strip() for tag in sections[i].select('span.visually-hidden')][0])
                section_head[head] = i+2
        return section_head
    #endregion


    #region GET SECTION's INFO
    def get_section_info(self, section_number: int, full_xpath: str, ):
        sleep(1)
        wait = WebDriverWait(self.driver,10)
        info_list = []
        show_more_check = False
        try:
            show_more = self.driver.find_element(By.XPATH, value= full_xpath + f'''/section[{section_number}]/div[3]/div/div/div/a''')
            show_more_check = True
        except NoSuchElementException:
            show_more_check = False

        if show_more_check:   #if yes: click show more
            wait.until(EC.element_to_be_clickable(show_more))
            show_more.click()
            sleep(2)
            infinite_scroll(self.driver)
            list_container = self.driver.find_element(By.CLASS_NAME, value='pvs-list__container')
            list_container_source = BeautifulSoup(list_container.get_attribute('outerHTML'),'html.parser')
            li_elements = list_container_source.find_all('div', class_='display-flex flex-column align-self-center flex-grow-1')

            for li in li_elements:
                span_tags = li.find_all('span', class_='visually-hidden')
                span_text = [tag.text.strip() for tag in span_tags]
                info_list.append(span_text) 
                    
            self.driver.back()
            
        else:
            ul_element = self.driver.find_element(By.XPATH, value=f'//*[@id="profile-content"]/div/div[2]/div/div/main/section[{section_number}]/div[3]/ul')

            ul_element_source = BeautifulSoup(ul_element.get_attribute('outerHTML'),'html.parser')
            number_of_li = len(ul_element_source.find_all('li',class_='artdeco-list__item'))

            if(number_of_li<2):
                # li_element = driver.find_element(By.XPATH, value='/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[3]/div[3]/ul/li/div/div[2]')
                li_element = self.driver.find_element(By.XPATH, value=f'//*[@id="profile-content"]/div/div[2]/div/div/main/section[{section_number}]/div[3]/ul/li/div/div[2]')
                li_element_source = BeautifulSoup(li_element.get_attribute('outerHTML'),'html.parser')
                span_tags = li_element_source.find_all('span', class_='visually-hidden')
                span_text = [tag.text.strip() for tag in span_tags]
                info_list.append(span_text)
            else:
                for j in range(number_of_li):
                    li_number = j+1
                    # li_element = driver.find_element(By.XPATH, value=f'//*[@id="profile-content"]/div/div[2]/div/div/main/section[{section_number}]/div[3]/ul/li[{li_number}]/div/div[2]')
                    li_element = self.driver.find_element(By.XPATH, value=f'//*[@id="profile-content"]/div/div[2]/div/div/main/section[{section_number}]/div[3]/ul/li[{li_number}]/div/div[2]')
                    li_element_source = BeautifulSoup(li_element.get_attribute('outerHTML'),'html.parser')
                    span_tags = li_element_source.find_all('span', class_='visually-hidden')
                    span_text = [tag.text.strip() for tag in span_tags]
                    info_list.append(span_text)    

        return info_list
    #endregion


    #region GET EXPERIENCE
    def get_experience(self,sections: dict, full_xpath: str) -> list:
        if 'Experience' in sections:
            section_number = sections['Experience']
            section_info = self.get_section_info(section_number, full_xpath)
            return section_info

        return None
    #endregion


    #region GET SKILLS
    def get_skills(self, sections: dict, full_xpath: str) -> list:
        if 'Skills' in sections:
            section_number = sections['Skills']
            section_info = self.get_section_info(section_number, full_xpath)
            return section_info

        return None
    #endregion


    #region GET EDUCATION
    def get_education(self, sections: dict, full_xpath: str) -> list:
        if 'Education' in sections:
            section_number = sections['Education']
            section_info = self.get_section_info(section_number, full_xpath)
            return section_info

        return None
    #endregion


    #region GET CERTIFICATION
    def get_cert(self, sections: dict, full_xpath: str) -> list:
        if 'Licenses & certifications' in sections:
            section_number = sections['Licenses & certifications']
            section_info = self.get_section_info(section_number, full_xpath)
            return section_info

        return None
    #endregion


    #region GET PROFILE INFO
    def get_profile_info(self, profile_url) -> dict:
        self.driver.get(profile_url)
        main_element = self.driver.find_element(By.CLASS_NAME, value='scaffold-layout__main')
        full_xpath = get_fullxpath(self.driver,main_element)
        sections = self.get_sections()
        profile_info = {
            'Contact Info': self.get_contact_info(),
            'Experience': self.get_experience(sections, full_xpath),
            'Education': self.get_education(sections, full_xpath),
            'Skills': self.get_skills(sections, full_xpath),
            'Licenses & certifications': self.get_cert(sections, full_xpath)
        }

        return profile_info
        
    #endregion
