import terminal
import inUtil
import outUtil
import importlib

def main():
    args = terminal.arguments()
    routerName =  args.name.upper()
    connectionType = args.type.lower()
    sshVar = args.ssh
    serialVar = args.serial
    jsonFile = args.file
    msg = args.msg
    if msg == None:
        msg = "Test"
    routerNameTest = ""

    if connectionType != "ssh" and connectionType != "serial":
        print("Bad connection type")
        quit()

    testing = importlib.import_module(connectionType + "Testing")

    if connectionType == "ssh":
        sc = testing.connectSSH(sshVar)
        routerNameTest, routerInfo = testing.deviceInfoSSH(sc)
    elif(connectionType == "serial"):
        ser = testing.connectSerial(serialVar)
        routerInfo = testing.deviceInfoSerial(ser)
    
    commands, expected = inUtil.readCommandFile(routerName, connectionType, jsonFile)
    print("Router being tested: " + routerName)
    
    if connectionType == "ssh":
        result, success = testing.testSSH(sc, commands, expected, msg)
    elif connectionType == "serial":
        result, success = testing.testSerial(ser, commands, expected, msg)

    fileName = outUtil.writeToCSV(commands, expected, result, success, routerName, routerInfo)
    outUtil.uploadToFTP(fileName)

if __name__ == "__main__":
    main()