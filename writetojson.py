import json

data = {}

lines = {}
variables = {}
def addtolines(jsnd, step):
    lines[step] = jsnd

def addtovars(jsnd, step):
    variables[step] = jsnd

def addtoothers(jsnd):
    data["others"] = jsnd
    