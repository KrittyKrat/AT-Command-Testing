import serial
import terminal
import time

def connectSerial():
    ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=5)
    time.sleep(0.1)

    return ser

def deviceInfoSerial(ser):
    ser.write(str.encode("ATI"+ "\r"))
    ser.readline()
    line1 = ser.readline().decode().split("\n")[0].strip()
    line2 = ser.readline().decode().split("\n")[0].strip()
    routerInfo = line2 + "\n" + line1

    return routerInfo

def testSerial(ser, commands, exp):
    success = []
    result = []
    passedCommands = 0
    failedCommands = 0
    totalCommands = len(commands)

    terminal.terminal("Current command", "Passed commands", "Failed commands", "All commands", False)

    for i in range(0, len(commands)):
        ser.write(str.encode(commands[i] + "\r"))
        time.sleep(0.1)
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