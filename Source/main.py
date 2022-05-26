import live_screen
import time
import read_email
from send_email import Mail
import traceback 

# đọc ảnh

# data=live_screen.capture_screen()
# with open('screen.png','wb') as f:
#     f.write(data)
while True:
    try:
        email_from, email_subject, email_body = read_email.read_email_from_gmail()
        if email_body == 'live_screen':
            data=live_screen.capture_screen()
            with open('screen.png','wb') as f:
                f.write(data)
            attach=[]
            attach.append('screen.png')
            print(1)
            mail=Mail()
            mail.sendMailWithAttach(email_from, email_subject, email_body, attach)
        break
            
    except Exception as e:
        traceback.print_exc() 
        print(str(e))
        print('Lỗi main.py')
        break
