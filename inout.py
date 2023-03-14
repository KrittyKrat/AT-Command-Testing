from datetime import datetime
import json
import csv

def readCommandFile(routerName, jsonFile):

    try:
        file = open(jsonFile)
        data = json.load(file)
    except:
        print("Failed to open the command file")
        quit()

    commands = []
    expected = []

    connected = False

    try:
        for d in data['devices']:
            if d['router'] == routerName:
                if routerName != d['router']:
                    print("Router not connected")
                    quit()
                for c in d['commands']:
                    commands.append(c['name'])
                    expected.append(c['expected'])
                connected = True
    except:
        print("Bad json format")
        quit()
        
    if not connected:
        print("No specified device found")
        quit()

    return commands, expected
    
def writeToCSV(commands, expected, result, success, routerName, routerInfo):
    fileName = "Results/" + routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    #file = open("Results/test.csv", 'w')
    file = open(fileName, 'w')
    writer = csv.writer(file)

    writer.writerow(["Model: " + routerInfo.split("\n")[0], "Manufacturer: " + routerInfo.split("\n")[1]])
    writer.writerow(["Command", "Expected", "Result", "Pass"])

    for i in range(0, len(commands)):
        writer.writerow([commands[i], expected[i], result[i], success[i]])