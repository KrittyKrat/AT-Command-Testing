from datetime import datetime
import csv
import paramiko
from email.mime.text import MIMEText
import smtplib
    
def writeToCSV(commands, expected, result, success, routerName, routerInfo):
    tempName = routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    fileName = "Results/" + tempName
    #file = open("Results/test.csv", 'w')
    
    try:
        file = open(fileName, 'w')
        writer = csv.writer(file)
    except:
        print("Failed to open file")
        quit()
    
    try:
        writer.writerow(["Model: " + routerInfo.split("\n")[0], "Manufacturer: " + routerInfo.split("\n")[1]])
        writer.writerow(["Command", "Expected", "Result", "Pass"])

        for i in range(0, len(commands)):
            writer.writerow([commands[i], expected[i], result[i], success[i]])
    except:
        print("Failed to write to .csv file")
        quit()
    
    file.close()
    return tempName

def uploadToFTP(fileName):
    host, port = "84.15.249.182", 22
    user, pasw = "akademija", "akademija"
    fileDir = "Results/" + fileName
    fileEndDir = "/home/akademija/ftp/" + fileName

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(None, user, pasw)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except:
        print("Failed to connect to the FTP server")
        quit()

    try:
        sftp.put(fileDir, fileEndDir)
    except:
        print("Failed to upload file to FTP server")
        quit()

    if sftp: sftp.close()
    if transport: transport.close()

def sendEmail(email):
    msg = MIMEText("This is a test")
    msg['Subject'] = "Test"
    msg['From'] = "teltonikaEmailTest@gmail.com"
    msg['To'] = email
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login("teltonikaEmailTest@gmail.com", "ahlyogorfmcjivyl")
    smtp_server.sendmail("teltonikaEmailTest@gmail.com", email, msg.as_string())
    smtp_server.quit()
    print("sent")