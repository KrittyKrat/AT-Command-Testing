import paramiko
import time
import terminal

def connectSSH(sshVar):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if sshVar == None:
            ssh_client.connect(hostname='192.168.1.1',username='root',password='Admin123', timeout=5)
        else:
            ssh_client.connect(hostname=sshVar[0],username=sshVar[1],password=sshVar[2], timeout=5)
    except:
        print("Wrong ssh variables")
        quit()
    
    executeCommand(ssh_client, "/etc/init.d/gsmd start")
    time.sleep(1)
    return ssh_client

def deviceInfoSSH(sc):
    stdin, stdout, stderr = executeCommand(sc, "uci get system.system.routername")
    routerName = stdout.read().decode().split("\n")[0]

    stdin, stdout, stderr = executeCommand(sc, "gsmctl -mw")
    routerInfo = stdout.read().decode()

    executeCommand(sc, "/etc/init.d/gsmd stop")

    return routerName, routerInfo

def testSSH(sc, commands, exp, msg):
    shell = sc.invoke_shell()
    shell.send("socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\r")
    time.sleep(0.1)
    rez = shell.recv(9999)
    
    result = []
    success = []

    passedCommands = 0
    failedCommands = 0
    totalCommands = len(commands)

    terminal.terminal("Current command", "Passed commands", "Failed commands", "All commands", False)
    shell.settimeout(2)

    for i in range(0, len(commands)):
        terminal.terminal(commands[i], passedCommands, failedCommands, totalCommands, True)
        try:
            shell.send(commands[i] + "\n")
            time.sleep(0.1)
            rez = shell.recv(9999).decode().split("\n")
            rez = list(filter(None, rez))

            if(commands[i].startswith("AT+CMGS") or commands[i].startswith("AT+CMGW") or commands[i].startswith("AT+CMSS")):
                shell.send(msg)
                shell.send(chr(26))
                time.sleep(2)
                rez = shell.recv(9999).decode().split("\n")
                rez = list(filter(None, rez))

            if rez[len(rez) - 1] == exp[i]:
                success.append(True)
                passedCommands += 1
            else:
                success.append(False)
                failedCommands += 1
            
            result.append(rez[len(rez) - 1])
            
        except:
            executeCommand(sc, 'ls')
            if(exp[i] == "ERROR"):
                success.append(True)
            else:
                success.append(False)
            result.append("ERROR")

    terminal.terminal("--------", passedCommands, failedCommands, totalCommands, False)
    executeCommand(sc, "/etc/init.d/gsmd start")
    sc.close()
    return result, success

def executeCommand(sc, command):
    try:
        stdin,stdout,stderr = sc.exec_command(command, timeout=1)
        return stdin,stdout,stderr
    except:
        print("\nConnection lost")
        quit()