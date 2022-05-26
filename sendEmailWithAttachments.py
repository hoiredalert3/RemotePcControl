import smtplib, ssl
import os
from email.message import EmailMessage

class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "controlcomputer20TN@gmail.com"
        self.password = "1!2@3#4$"

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()

    def sendMailWithAttach(self, emails, subject, content, attachment_names):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_mail
        msg['To'] = emails
        msg.set_content(content)

        for file_name in attachment_names:
            with open(file_name, 'rb') as f:
                data = f.read()
                name = f.name #Attribute chu khong phai method
                msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as service:
            service.login(self.sender_mail, self.password)
            service.send_message(msg)




if __name__ == '__main__':
    mails = input("Enter emails: ").split()
    subject = input("Enter subject: ")
    content = input("Enter content: ")

    mail = Mail()
    #mail.send(mails, subject, content)
    attachments = os.listdir()
    mail.sendMailWithAttach(mails, subject, content, attachments)