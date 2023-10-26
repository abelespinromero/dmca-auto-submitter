import imaplib
import email
from datetime import datetime, timedelta
import pandas as pd
import time

imaplib._MAXLINE = 100000000

def reconnect_mail_service(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail

def fetch_email(mail, email_id, text_data, debug):
    try:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text = part.get_payload(decode=True)
                if text:
                    text = text.decode(errors='replace').strip()
                    text_data.append(text)
                    if debug:
                        print(f"Correo {len(text_data)} procesado.")
    except Exception as e:
        print(f"Error al procesar el correo {email_id}: {str(e)}")
        raise e

def scrape_emails(email, app_password, date_limit="historical", debug=False):
    username = email
    password = app_password
    text_data = []
    adaptive_wait_time = 5
    email_ids_processed = set()

    try:
        mail = reconnect_mail_service(username, password)
        subject_filter = 'Notice of DMCA removal from Google Search'

        if date_limit == "historical":
            status, email_ids = mail.search(None, 'SUBJECT', f'"{subject_filter}"')
        else:
            now = datetime.now()
            one_day_ago = now - timedelta(days=1)
            date_limit = one_day_ago.strftime('%d-%b-%Y')
            status, email_ids = mail.search(None, f'(SINCE "{date_limit}") SUBJECT "{subject_filter}"')

        email_ids = email_ids[0].split()
        batch_size = 100

        for i in range(0, len(email_ids), batch_size):
            for email_id in email_ids[i:i+batch_size]:
                if email_id not in email_ids_processed:
                    try:
                        fetch_email(mail, email_id, text_data, debug)
                        email_ids_processed.add(email_id)
                    except Exception as e:
                        mail = reconnect_mail_service(username, password)
                        adaptive_wait_time += 5
                        time.sleep(adaptive_wait_time)

            if debug:
                print(f"{len(text_data)} emails downloaded so far.")

            time.sleep(adaptive_wait_time)
            
    except imaplib.IMAP4.error as e:
        print(e)
        print("Failed to log in with application password.")
    finally:
        mail.logout()

    df = pd.DataFrame({"email_text": text_data})
    if debug:
        df.to_csv("emails_text.csv")

    return df

# Ejemplo de uso
# df = scrape_emails(date_limit="hourly", debug=True)
# print(df)
