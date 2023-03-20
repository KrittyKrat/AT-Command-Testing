from email.mime.text import MIMEText
import smtplib
from datetime import datetime

def sendEmail(email, routerName, uploadData):
    tempName = routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    msg = MIMEText("Test: " + tempName + ", has been completed")
    msg['Subject'] = routerName + " at command test"
    msg['From'] = uploadData.email
    msg['To'] = email
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(uploadData.email, uploadData.emailpas)
    smtp_server.sendmail(uploadData.email, email, msg.as_string())
    smtp_server.quit()