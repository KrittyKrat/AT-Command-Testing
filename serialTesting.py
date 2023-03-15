import serial
import terminal
import time
import os

def connectSerial(serialVar):
    try:
        if serialVar == None:
            os.system("sudo chmod 666 /dev/ttyUSB3")
            ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=5)
        else:
            os.system("sudo chmod 666 " + serialVar[0])
            ser = serial.Serial(serialVar[0], serialVar[1], timeout=5)
    except:
        print("Could not connect to serial port")
        quit()

    time.sleep(0.1)
    return ser

def deviceInfoSerial(ser):
    
    try:
        ser.write(str.encode("ATI"+ "\r"))
        ser.readline()
    except:
        print("Failed to get router info")
        quit()

    line1 = ser.readline().decode().split("\n")[0].strip()
    line2 = ser.readline().decode().split("\n")[0].strip()

    while(True):
        l = ser.readline().decode().split("\n")[0].strip()
        if l == "OK":
            break

    routerInfo = line2 + "\n" + line1

    return routerInfo

def testSerial(ser, commands, exp, msg):
    success = []
    result = []
    passedCommands = 0
    failedCommands = 0
    totalCommands = len(commands)
    ser.timeout = 1

    terminal.terminal("Current command", "Passed commands", "Failed commands", "All commands", False)

    for i in range(0, len(commands)):
        terminal.terminal(commands[i], passedCommands, failedCommands, totalCommands, True)

        try:
            ser.write(str.encode(commands[i] + "\r"))
            ser.flush()
            time.sleep(0.1)

            checkMessage(commands[i], msg, ser)
            result, success = findResult(ser, result, success, exp[i])

        except:
            print("\nConnection lost")
            quit()
        
        passedCommands, failedCommands = determineScore(success[len(success) - 1], passedCommands, failedCommands)

    ser.close()
    terminal.terminal("--------", passedCommands, failedCommands, totalCommands, False)
    return result, success

def findSuccess(expected, gotten):
    if gotten == expected:
        return True
    else:
        return False
    
def determineScore(result, passedCommands, failedCommands):
    if result:
        passedCommands += 1
    else:
        failedCommands += 1
    return passedCommands, failedCommands

def findResult(ser, result, success, ex):
    counter = 0
    while(True):
        counter = counter + 1
        line = ser.readline().decode().strip()

        if line == "OK" or line == "ERROR":
            result.append(line)
            success.append(findSuccess(line, ex))
            break

        if len(line) == 0 and counter <= 1:
            result.append("ERROR")
            success.append(findSuccess("ERROR", ex))
            break

    return result, success

def checkMessage(command, msg, ser):
    if(command.startswith("AT+CMGS") or command.startswith("AT+CMGW") or command.startswith("AT+CMSS")):
        ser.write(str.encode(msg))
        ser.write(str.encode(chr(26)))
        time.sleep(1)