import json

data = {}
data2 = {}

lines = {}
variables = {}
def addtolines(jsnd, step):
    lines[step] = jsnd

def addtovars(jsnd, step):
    variables[step] = jsnd

def addtoothers(jsnd):
    data["others"] = jsnd

def findata():
    data["variables"] = variables
    data["lines"] = lines

def dumpjson():
    with open('data.json', 'w') as fp:
        json.dump(data, fp)