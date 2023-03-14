import paramiko
import time
import terminal

def connectSSH(sshVar):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if sshVar == None:
            ssh_client.connect(hostname='192.168.1.1',username='root',password='Admin123')
        else:
            ssh_client.connect(hostname=sshVar[0],username=sshVar[1],password=sshVar[2])
    except:
        print("Wrong ssh variables")
        quit()

    return ssh_client

def deviceInfoSSH(sc):
    stdin,stdout,stderr=sc.exec_command("uci get system.system.routername")
    routerName = stdout.read().decode().split("\n")[0]

    stdin,stdout,stderr=sc.exec_command("gsmctl -mw")
    routerInfo = stdout.read().decode()

    sc.exec_command("/etc/init.d/gsmd stop")

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

    for i in range(0, len(commands)):
        shell.send(commands[i] + "\n")
        time.sleep(0.1)
        rez = shell.recv(9999).decode().split("\n")
        rez = list(filter(None, rez))

        if rez[len(rez) - 1] == exp[i]:
            success.append(True)
            passedCommands += 1
        else:
            success.append(False)
            failedCommands += 1
        
        result.append(rez[len(rez) - 1])
        terminal.terminal(commands[i], passedCommands, failedCommands, totalCommands, True)

    terminal.terminal("--------", passedCommands, failedCommands, totalCommands, False)
    sc.exec_command("/etc/init.d/gsmd start")
    sc.close()
    return result, success