import json

def openJson(jsonFile):
    try:
        file = open(jsonFile)
        data = json.load(file)
    except:
        print("Failed to open the command file")
        quit()

    return file, data

def readCommandFile(routerName, connectionType, jsonFile):

    file, data = openJson(jsonFile)
    commands = []
    expected = []
    connected = False

    try:
        for d in data['devices']:
            if d['router'] == routerName:
                if connectionType != d['type']:
                    break
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

    file.close()
    return commands, expected