from email.mime.text import MIMEText
import smtplib
from datetime import datetime

def sendEmail(email, routerName):
    tempName = routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    msg = MIMEText("Test: " + tempName + ", has been completed")
    msg['Subject'] = routerName + " at command test"
    msg['From'] = "teltonikaEmailTest@gmail.com"
    msg['To'] = email
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login("teltonikaEmailTest@gmail.com", "ahlyogorfmcjivyl")
    smtp_server.sendmail("teltonikaEmailTest@gmail.com", email, msg.as_string())
    smtp_server.quit()