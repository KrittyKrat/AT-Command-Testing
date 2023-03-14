import serial
import terminal
import time
import os

def connectSerial(serialVar):
    #os.system("sudo systemctl stop ModemManager.service")
    os.system("sudo chmod 666 /dev/ttyUSB3")

    try:
        if serialVar == None:
            ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=5)
        else:
            ser = serial.Serial(serialVar, 115200, timeout=5)
    except:
        print("Could not connect to serial port")
        quit()

    time.sleep(0.1)
    return ser

def deviceInfoSerial(ser):
    ser.write(str.encode("ATI"+ "\r"))
    ser.readline()
    line1 = ser.readline().decode().split("\n")[0].strip()
    line2 = ser.readline().decode().split("\n")[0].strip()
    routerInfo = line2 + "\n" + line1

    return routerInfo

def testSerial(ser, commands, exp, msg):
    success = []
    result = []
    passedCommands = 0
    failedCommands = 0
    totalCommands = len(commands)

    terminal.terminal("Current command", "Passed commands", "Failed commands", "All commands", False)

    for i in range(0, len(commands)):

        ser.write(str.encode(commands[i] + "\r"))
        time.sleep(0.1)

        if(commands[i].startswith("AT+CMGS") or commands[i].startswith("AT+CMGW") or commands[i].startswith("AT+CMSS")):
            ser.write(str.encode(msg))
            ser.write(str.encode(chr(26)))
            time.sleep(1)

        ser.readline()

        while(True):
            line = ser.readline().decode().split("\n")[0].strip()

            if line == "OK" or line == "ERROR":
                result.append(line)
                if line == exp[i]:
                    success.append(True)
                    passedCommands += 1
                    break
                else:
                    success.append(False)
                    failedCommands += 1
                    break

        terminal.terminal(commands[i], passedCommands, failedCommands, totalCommands, True)

    
    ser.close()
    terminal.terminal("--------", passedCommands, failedCommands, totalCommands, False)
    return result, success