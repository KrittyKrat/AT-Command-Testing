from modules import terminal_utility
from modules import read_file_utility
from modules import print_file_utility
from modules import uploadEmail
from modules import uploadFTP
import importlib

def main():
    args = terminal_utility.arguments()
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
    
    commands, expected, uploadData = read_file_utility.readCommandFile(routerName, connectionType, jsonFile)
    print("Router being tested: " + routerName)
    
    if connectionType == "ssh":
        result, success = testing.testSSH(sc, commands, expected, msg)
    elif connectionType == "serial":
        result, success = testing.testSerial(ser, commands, expected, msg)

    fileName = print_file_utility.writeToCSV(commands, expected, result, success, routerName, routerInfo)
    if email != None:
        uploadEmail.sendEmail(email, routerName, uploadData)
    uploadFTP.uploadToFTP(fileName, uploadData)

if __name__ == "__main__":
    main()