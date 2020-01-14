import json
from datetime import datetime

dta = {}

def main(pth):
    with open(pth, 'r') as f:
        dta = json.load(f)
    n = len(dta["lines"])
    print("----------------------------------------------")
    print("                     REPORT                   ")
    print("----------------------------------------------")
    print("                     SOURCE                   ")
    print("----------------------------------------------")
    print(dta["source"])
    print("----------------------------------------------")
    print("                     LINES                    ")
    print("----------------------------------------------")
    for i in range(1, n+1):
        print("At time %s," % (datetime.fromtimestamp(dta["lines"][str(i)]["timestamp"])), end = " ")
        curr = dta["lines"][str(i)]["report"]
        print("starting line %s" % (curr[0]))
        print("The time spent on this line is {:f} seconds".format(curr[1]))
        print("This line has been executed %s times before." % (curr[2]))
        print("The aggregate time spent on this line till now is {:f} seconds".format(curr[3]))
        print("The average time spent on this line till now is {:f} seconds".format(curr[4]))
        for j in curr[5]:
            varchanges = "In line %s, the value %s has been added to %s" % (curr[0], j[1], j[0])
            print(varchanges)
        for j in curr[6]:
            varchanges = "In line %s, the index %s of list %s has changed value from %s to %s" % (curr[0], j[1], j[0], j[2], j[3])
            print(varchanges)
        for j in curr[7]:
            varchanges = "In line %s, the variable %s has been initialized to %s" % (curr[0], j[0], j[1])
            print(varchanges)
        for j in curr[8]:
            varchanges = "In line %s, the variable %s has been changed value from %s to %s" % (curr[0], j[0], j[1], j[2])
            print(varchanges)
        for j in curr[9]:
            varchanges = "In line %s, the variable %s has been initialized to %s" % (curr[0], j[0], j[1])
            print(varchanges)
        print("----------------------------------------------")
    print("                   VARIABLES                  ")
    print("----------------------------------------------")
    for i in dta["variables"]:
        print("Tracing the variable " + i + " of type %s:-" % (dta["variables"][i]["type"])) 
        print("It was initialized on line %s" % (dta["variables"][i]["report"][1]))
        if(dta["variables"][i]["type"] == "int"):
            mnval = dta["variables"][i]["report"][2]
            mxval = dta["variables"][i]["report"][2]
            lastval = dta["variables"][i]["report"][2]
            print("The initial value of the variable was %s" % (lastval))
            for j in dta["variables"][i]["report"][3]:
                print("In line %s, the variable %s changed values from %s to %s"%(j[0], i, j[1], j[2]))
                lastval = j[2]
                mnval = min(j[2], mnval)
                mxval = max(j[2], mxval)
            print("The value of the variable ranges from %s to %s" % (mnval, mxval))
            print("The final value of the variable is %s" % (lastval))
        else: 
            lastval = dta["variables"][i]["report"][2]
            print("The initial value of the variable was %s" % (lastval))
            for j in dta["variables"][i]["report"][3]:
                print("In line %s, the variable %s changed values from %s to %s"%(j[0], i, j[1], j[2]))
                lastval = j[2]
            print("The final value of the variable is %s" % (lastval))
        print("----------------------------------------------")
    cnt= 0
    print("               OTHER INFORMATION              ")
    print("----------------------------------------------")
    for i in dta["others"]["report"]:
        cnt+=1
        if(cnt == 1):
            print("The program finished in {:f} seconds".format(curr[3]))
            print("----------------------------------------------")
        else:
            if int(i[1]) != 1:
                print("Line %s was executed %s times" % (i[0], i[1]))
            else:
                print("Line %s was executed %s time" % (i[0], i[1]))
    print("----------------------------------------------")