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
    print("                     LINES                    ")
    print("----------------------------------------------")
    for i in range(1, n+1):
        print("At time %s," % (datetime.fromtimestamp(dta["lines"][str(i)]["timestamp"])), end = " ")
        for j in dta["lines"][str(i)]["report"]:
            print(j)
        print("----------------------------------------------")
    print("                   VARIABLES                  ")
    print("----------------------------------------------")
    for i in dta["variables"]:
        for j in dta["variables"][i]["report"]:
            print(j)
        print("----------------------------------------------")
    cnt= 0
    for i in dta["others"]["report"]:
        print(i)
        cnt+=1
        if(cnt == 1):
            print("----------------------------------------------")
    print("----------------------------------------------")