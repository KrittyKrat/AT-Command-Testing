# AT Command Testing Thing

#### Intro
This is a a simple python program designed to test the functionality of AT commands in any **RUTXxx** and **RUT9xx** series routers, as well as the **TRM2xx** series modems.
#### Prerequisites
Before you begin these are the libraries you will need to install:
```
pip install paramiko
pip install pyserial
pip install argparse
```
You will also need to disable the ModemManager process for the serial connection to work:
```
sudo systemctl stop ModemManager.service
```
#### Program
First you must connect your desired device to your computer either using an ethernet or serial cable. You can run the program using:
```
python3 at.py [--name] "router name" [--file] "command file location" [--type] "connection type" [--ssh] "ssh variables"
```
The router name, file and connection type are mandatory arguments and must be pasted correctly. Ssh variables are optional if you decide to use an ssh type connection and want to set your own variables for the hostname, user and password. Here are a few examples of how to use the program:
```
python3 at.py --name RUTX11 --file Commands/commands.json --type ssh
python3 at.py --name RUT955 --file /home/stud/testCom.json --type ssh --ssh 192.168.1.1 root admin
python3 at.py --name TRM240 --file Commands/commands2.json --type serial
```
While running the program you will be able to see live results like the command being tested, total number of commands to be tested, how many commands passed and failed the test.
#### Files
The command file must be a .json and it is formated like this:
```
{
  "devices": [
    {
      "router":"RUTX11",
      "commands": [
        {
          "name":"AT+GMR",
          "expected": "OK"
        },
        {
          "name":"AT+TEST",
          "expected": "ERROR"
        }
      ]
    },
    {
      "router":"TRM240",
      "commands": [
        {
          "name":"ATE1",
          "expected": "OK"
        },
        {
          "name":"ATI",
          "expected": "OK"
        },
        {
          "name":"AT+CMGF=1",
          "expected": "OK"
        }
      ]
    }
  ]
}
```
Results are stored in the Results folder in .csv format. A new file is created for every time you launch a test.