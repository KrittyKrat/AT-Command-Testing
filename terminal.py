import argparse

class cl:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def terminal(currentCommand, passedCommands, failedCommands, totalCommands, override):
    if override:
        print(f"{currentCommand:25} | {cl.OKGREEN}{passedCommands:15}{cl.ENDC} | {cl.FAIL}{failedCommands:15}{cl.ENDC} | {totalCommands:12} |", end='\r')
    else:
        print(f"{currentCommand:25} | {cl.OKGREEN}{passedCommands:15}{cl.ENDC} | {cl.FAIL}{failedCommands:15}{cl.ENDC} | {totalCommands:12} | \r")

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the router', required=True)
    parser.add_argument('--file', type=str, help='Name of the command .json file', required=True)
    parser.add_argument('--type', type=str, help='Connection type (ssh/serial)', required=True)
    parser.add_argument('--ssh', type=str, help='Ssh variables (ip, username, password)', nargs=3, required=False)
    parser.add_argument('--serial', type=str, help='Custom serial port (/dev/ttyUSBx, baudrate)', nargs=2, required=False)
    parser.add_argument('--msg', type=str, help='Custom message to test send message at command', required=False)
    args = parser.parse_args()
    return args