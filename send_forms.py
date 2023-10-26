from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.firefox.options import Options
from capmonster_python import RecaptchaV2Task


import time
import pandas as pd

def create_webdriver():
    # Create an Options object
    options = Options()
    # Point to the profile directory to automatic logging
    options.profile = 'C://Users//<your-user>//AppData//Roaming//Mozilla//Firefox//Profiles//<your-profile>' #Change
    # Set additional preferences
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    # Initialize the driver
    driver = webdriver.Firefox(options=options)

    return driver


def open_form(driver, url):
    # Abrir la URL
    driver.get(url)

def fill_form(driver, country=" ", name=" ", title=" ", company=" ", address=" ", form_email=" ", phone_number=" ", details=" ", signature=" ", urls=" "):
    # Localizar los campos del formulario y completarlos
    
    # Country of residence
    country_of_residence_button = driver.find_element(By.XPATH, '//*[contains(@class, "sc-select")]')
    country_of_residence_button.click()

    especific_country_button = driver.find_element(By.XPATH, f'//li[text()="{country}"]')
    especific_country_button.click()
    
    # Full legal name
    full_legal_name_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Full legal name")]')  
    full_legal_name_elem.send_keys(name)  # Ingresa tu nombre completo

    # Your Title
    your_title_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Your Title")]')
    your_title_elem.send_keys(title)

    # Company Name
    company_name_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Company Name")]')
    company_name_elem.send_keys(company)

    # Contact email address
    #contact_email_address_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Contact email address")]')
    #contact_email_address_elem.send_keys(form_email)

    # Address
    adress_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Address")]')
    adress_elem.send_keys(address)    

    # Phone number
    phone_number_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Phone number")]')
    phone_number_elem.send_keys(phone_number)        

    # Urls
    urls_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "URL(s) of the content in question")]')
    for url in urls:
        urls_elem.send_keys(url + "\n")

    # Why are you requesting reinstatement?
    driver.execute_script("document.getElementById('dmca_clarifications_intro--counternotice.clarify_noright').click();")

    # Please provide more details to justify your request
    details_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Please provide more details to justify your request")]')
    details_elem.send_keys(details)

    # Sworn statements accept
    driver.execute_script("document.getElementById('consent_statement1--dmca_consent_statement').click();")
    driver.execute_script("document.getElementById('consent_statement2--dmca_consent_statementtwo').click();")
    driver.execute_script("document.getElementById('consent_statement3--dmca_consent_statement3').click();")

    # Signature
    signature_elem = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Signature")]')
    signature_elem.send_keys(signature)

    # Feedback
    # driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[contains(@id, "rce")]'))

def send_form(driver):
    # Envía el formulario (puede variar según el sitio web)
    driver.find_element(By.XPATH, '//*[contains(@class, "submit-button material2-button material2-button--filled")]').click()  # Cambia "submit" por el nombre del botón de envío real

def resolve_recaptcha(driver, api_key, site_key, url):
    capmonster = RecaptchaV2Task(api_key)
    task_id = capmonster.create_task(url, site_key)
    result = capmonster.join_task_result(task_id)
    solved=False
    while not solved:
        if result.get("gRecaptchaResponse"):
            g_recaptcha_response = result.get("gRecaptchaResponse")
            # Resuelve el reCAPTCHA
            driver.execute_script("document.getElementById('g-recaptcha-response-1').innerHTML = "+"'" + g_recaptcha_response + "'")
            solved = True
        time.sleep(3)  # Esperar antes de verificar nuevamente

def check_if_submitted(driver, count):
    try:
        _ = driver.find_element(By.XPATH, '//textarea[@id="g-recaptcha-response"]')
        submited = False
        print("Form not submitted")
    except:
        print(f"Form {count} submitted")
        count+=1
        submited = True
    return submited, count

def finish_webdriver(driver):
    driver.quit()

# Main
#driver = create_webdriver()
#open_form(driver)
#fill_form(driver)
#send_form(driver)
#resolve_recaptcha(driver, api_key, site_key, url)
#send_form(driver)