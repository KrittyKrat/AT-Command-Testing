import terminal
import inout
import importlib

def main():
    args = terminal.arguments()
    routerName =  args.name
    connectionType = args.type
    sshVar = args.ssh
    jsonFile = args.file
    routerNameTest = ""

    if connectionType != "ssh" and connectionType != "serial":
        print("Bad connection type")
        quit()

    testing = importlib.import_module(connectionType + "Testing")

    if connectionType == "ssh":
        sc = testing.connectSSH(sshVar)
        routerNameTest, routerInfo = testing.deviceInfoSSH(sc)
    elif(connectionType == "serial"):
        ser = testing.connectSerial()
        routerInfo = testing.deviceInfoSerial(ser)
    
    commands, expected = inout.readCommandFile(routerName, jsonFile)
    print("Router being tested: " + routerName)
    
    if connectionType == "ssh":
        result, success = testing.testSSH(sc, commands, expected)
    elif connectionType == "serial":
        result, success = testing.testSerial(ser, commands, expected)

    inout.writeToCSV(commands, expected, result, success, routerName, routerInfo)

if __name__ == "__main__":
    main()
