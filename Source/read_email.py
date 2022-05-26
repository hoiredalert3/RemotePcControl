import imaplib
import email
import traceback 

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "controlcomputer20TN" + ORG_EMAIL
FROM_PWD = "1!2@3#4$"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        latest_email_id = int(id_list[-1])

        i = latest_email_id
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                email_from = str(msg['from'])
                # email_from=email_from['<':'>']
                i = 0
                j = 0
                for k in range(len(email_from)):
                    if email_from[k] == '<':
                        i = k
                    if email_from[k] == '>':
                        j = k
                        break
                email_from = email_from[i+1:j]
                email_subject = str(msg['subject'])
                payload = msg.get_payload()[0]
                email_body = str(payload.get_payload())
                email_body = email_body[:len(email_body)-2]
        return email_from, email_subject, email_body

    except Exception as e:
        traceback.print_exc() 
        print(str(e))
        print('Lỗi đọc email')
        return 0, 0, 0
