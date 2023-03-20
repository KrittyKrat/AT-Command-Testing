from modules import terminal
from modules import inUtil
from modules import outUtil
from modules import uploadEmail
from modules import uploadFTP
import importlib

def main():
    args = terminal.arguments()
    routerName =  args.name.upper()
    connectionType = args.type.lower()
    sshVar = args.ssh
    serialVar = args.serial
    jsonFile = args.file
    msg = args.msg
    email = args.email
    
    if msg == None:
        msg = "Test"
    routerNameTest = ""

    if connectionType != "ssh" and connectionType != "serial":
        print("Bad connection type")
        quit()

    testing = importlib.import_module("modules." + connectionType + "Testing")

    if connectionType == "ssh":
        sc = testing.connectSSH(sshVar)
        routerNameTest, routerInfo = testing.deviceInfoSSH(sc)
    elif(connectionType == "serial"):
        ser = testing.connectSerial(serialVar)
        routerInfo = testing.deviceInfoSerial(ser)
    
    commands, expected, uploadData = inUtil.readCommandFile(routerName, connectionType, jsonFile)
    print("Router being tested: " + routerName)
    
    if connectionType == "ssh":
        result, success = testing.testSSH(sc, commands, expected, msg)
    elif connectionType == "serial":
        result, success = testing.testSerial(ser, commands, expected, msg)

    fileName = outUtil.writeToCSV(commands, expected, result, success, routerName, routerInfo)
    if email != None:
        uploadEmail.sendEmail(email, routerName, uploadData)
    uploadFTP.uploadToFTP(fileName, uploadData)

if __name__ == "__main__":
    main()