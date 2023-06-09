import paramiko

def uploadToFTP(fileName, uploadData):
    host, port = uploadData.ftpip, uploadData.ftpport
    user, pasw = uploadData.ftpuser, uploadData.ftppas
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