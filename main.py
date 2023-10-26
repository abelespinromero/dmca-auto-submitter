from scrape_emails import scrape_emails
import extract_urls
import send_forms
from forms_data import URL, COUNTRY, NAME, TITLE, COMPANY, EMAILS, APP_PASSWORDS, ADDRESS, FORM_EMAIL, PHONE_NUMBER, DETAILS, SIGNATURE, API_CAPTCHA_KEY, SITE_CAPTCHA_KEY

from selenium.webdriver.common.by import By

import pandas as pd
import time

#MAIN

def main(date_limit="daily", debug=False):
    for email, app_password in zip(EMAILS, APP_PASSWORDS):
        #Scrape emails
        #emails_df = scrape_emails(email, app_password, date_limit=date_limit, debug=debug)
        emails_df = pd.read_csv("emails_text_first.csv")

        print("\nNotices scraped for {email}: ", len(emails_df))

        # Extract urls from emails
        urls_df = extract_urls.extract_all_urls(emails_df=emails_df, debug=debug)

        print(f"Urls from notices extracted for {email}. Total urls: {urls_df['urls'].apply(len).sum()}\n")

        #Submit forms:
        driver = send_forms.create_webdriver()
        
        count = 0
        for index, notice in urls_df.iterrows():
            
            urls = notice["urls"]
            
            # Agregar manejo de errores y reintento aquí
            retries = 0
            max_retries = 3 #Nº maximo de intentos

            while retries < max_retries:
                try:
                    send_forms.open_form(driver, URL)
                    send_forms.fill_form(driver, COUNTRY, NAME, TITLE, COMPANY, ADDRESS, FORM_EMAIL, PHONE_NUMBER, DETAILS, SIGNATURE, urls)
                    send_forms.send_form(driver)
                    try:
                        driver.find_element(By.XPATH, '//textarea[@id="g-recaptcha-response"]')
                        send_forms.resolve_recaptcha(driver, API_CAPTCHA_KEY, SITE_CAPTCHA_KEY, URL)
                        send_forms.send_form(driver)
                    except:
                        pass
                    
                    time.sleep(3)
                    submited,count = send_forms.check_if_submitted(driver, count)

                    if submited:
                        break # Si se envía correctamente, sal del bucle de reintento
                    
                    else:
                        print(f"Error submitting form (Attempt {retries + 1}): {'Captcha not passed'}")
                        retries += 1 
                        time.sleep(5)

                except Exception as e:
                    print(f"Error submitting form (Attempt {retries + 1}): {str(e)}")
                    retries += 1 
                    time.sleep(5)

        # Cierra el navegador al finalizar
        send_forms.finish_webdriver(driver)

        print(f"Number of submitted forms for {email}: {count}")
        print(f"Notices scraped == Submitted forms? {len(emails_df) == count}")


if __name__ == '__main__':
    main(date_limit="historical", debug=True)