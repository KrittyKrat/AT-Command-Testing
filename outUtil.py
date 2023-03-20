from datetime import datetime
import csv

def writeToCSV(commands, expected, result, success, routerName, routerInfo):
    tempName = routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    fileName = "Results/" + tempName
    #file = open("Results/test.csv", 'w')
    
    try:
        file = open(fileName, 'w')
        writer = csv.writer(file)
    except:
        print("Failed to open file")
        quit()
    
    try:
        writer.writerow(["Model: " + routerInfo.split("\n")[0], "Manufacturer: " + routerInfo.split("\n")[1]])
        writer.writerow(["Command", "Expected", "Result", "Pass"])

        for i in range(0, len(commands)):
            writer.writerow([commands[i], expected[i], result[i], success[i]])
    except:
        print("Failed to write to .csv file")
        quit()
    
    file.close()
    return tempName