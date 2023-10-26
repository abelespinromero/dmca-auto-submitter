import pandas as pd
import regex as re

def extract_all_urls(emails_df, debug=False):

    # Aplicar la función a la columna 'email_text'
    emails_df['urls'] = emails_df['email_text'].apply(extract_urls)


    # Save csv
    if debug:
        emails_df.to_csv("emails_text_urls.csv")


    return emails_df




# Función para extraer todos los URLs
def extract_urls(text):

    urls = re.findall(r'https?://[^\s]+', text)
    urls = urls[2:]
    return urls
    

# Main test
# urls_list = extract_all_urls()
# print(urls_list)