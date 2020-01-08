import sys
import copy
import time
import timeit
import importlib
import writetojson
import outputjson
from inspect import isfunction, getmembers

variablevalues = {}
answerint = {}
answerother = {}
aggtimeperline = {}
nooftimesperline = {}

step = 0

def trace_main(frame, event, args):
    if(event != 'call'):
        return 
    return trace_varchanges


print("----------------------------------------------")
print("                 TAKING INPUT                 ")
print("----------------------------------------------")
pth2 = input("Enter the name of the file you want to debug: ")
if pth2.find(".json") != -1:
    print("You entered a JSON file, reporting the data...")
    outputjson.main(pth2)
    exit()
if pth2.find(".py") == -1:
    print("Invalid file, breaking the program")
    exit()
fname = input("Enter the name of the function you want to debug: ")
pth = pth2.replace(".py", "")
modle = importlib.import_module(pth)
if(not hasattr(modle, fname)):
    print("Invalid input! Either wrong function name or wrong path!")
    exit()

print("----------------------------------------------")
print("              RUNNING FUNCTION                ")
print("----------------------------------------------")

def trace_varchanges(frame, event, args):
    global step
    if event != "line":
        return
    code = frame.f_code
    localvars = frame.f_locals
    line_no = frame.f_lineno-1
    arr = []
    strt = "Starting line %s ..." % (line_no)
    arr.append(strt)
    start_time = time.time()
    step+=1
    for i in code.co_varnames:
        if i in localvars:
            if(isinstance(localvars[i], list)):
                if i not in variablevalues:
                    line_no = frame.f_lineno-1
                    func_name = code.co_name
                    varchanges = "In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i])
                    arr.append(varchanges)
                    variablevalues[i] = []
                    variablevalues[i] = localvars[i][:]
                    answerother[i] = [line_no, type(localvars[i]), [[line_no, variablevalues[i]]]]
                else:
                    changed = False
                    if (len(variablevalues[i]) < len(localvars[i])):
                        line_no = frame.f_lineno-1
                        func_name = code.co_name
                        for j in range(len(variablevalues[i])):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                varchanges = "In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j])
                                arr.append(varchanges)
                                changed = True
                        for j in range(len(variablevalues[i]), len(localvars[i])):
                            varchanges = "In line %s of the %s function in the file %s, the value %s has been added to %s" % (line_no, func_name, code.co_filename, localvars[i][j], i)
                            arr.append(varchanges)
                            changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    else:
                        line_no = frame.f_lineno-1
                        func_name = code.co_name
                        for j in range(min(len(variablevalues[i]), len(localvars[i]))):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                varchanges = "In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j])
                                arr.append(varchanges)
                                changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    if changed == True:
                        answerother[i][2].append([line_no, variablevalues[i]])
            else:
                if i not in variablevalues:
                    line_no = frame.f_lineno-1
                    func_name = code.co_name
                    varchanges = "In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i])
                    arr.append(varchanges)
                    if(isinstance(localvars[i], int)):
                        answerint[i] = [line_no, localvars[i], localvars[i], [[line_no, localvars[i]]]]
                    else:
                        if(isinstance(localvars[i], tuple) or isinstance(localvars[i], dict) or isinstance(localvars[i], set)):
                            temp = localvars[i].copy()
                        else:
                            temp = localvars[i]
                        answerother[i] = [line_no, type(localvars[i]), [[line_no, temp]]]
                    if(isinstance(localvars[i], tuple) or isinstance(localvars[i], dict) or isinstance(localvars[i], set)):
                        variablevalues[i] = localvars[i].copy()
                    else:
                        variablevalues[i] = localvars[i]
                else:
                    if(localvars[i] != variablevalues[i]):
                        line_no = frame.f_lineno-1
                        func_name = code.co_name
                        varchanges = "In line %s of the %s function in the file %s, the variable %s has changed from %s to %s" % (line_no, func_name, code.co_filename, i, variablevalues[i], localvars[i])
                        arr.append(varchanges)
                        if(isinstance(localvars[i], int)):
                            answerint[i][1] = min(answerint[i][1], localvars[i])
                            answerint[i][2] = max(answerint[i][2], localvars[i])
                            answerint[i][3].append([line_no, localvars[i]])
                        else:
                            if(isinstance(localvars[i], tuple) or isinstance(localvars[i], dict) or isinstance(localvars[i], set)):
                                temp = localvars[i].copy()
                            else:
                                temp = localvars[i]
                            answerother[i][2].append([line_no, temp])
                            
                        if(isinstance(localvars[i], tuple) or isinstance(localvars[i], dict) or isinstance(localvars[i], set)):
                            variablevalues[i] = localvars[i].copy()
                        else:
                            variablevalues[i] = localvars[i]
    line_no = frame.f_lineno-1
    if line_no not in nooftimesperline:
        nooftimesperline[line_no] = 1
    else:
        nooftimesperline[line_no]+=1
    spent = time.time() - start_time
    if line_no not in aggtimeperline:
        aggtimeperline[line_no] = spent
    else:
        aggtimeperline[line_no]+=spent
    varchanges = "Time spent on this line is {:f} seconds.".format(spent)
    arr.append(varchanges)
    if(nooftimesperline[line_no] > 1):
        varchanges = "This line has been executed %s times before."%(nooftimesperline[line_no])
        arr.append(varchanges)
    else:
        varchanges = "This line has been executed %s time before."%(nooftimesperline[line_no])
        arr.append(varchanges)
    varchanges = "The aggregate time spent on this line till now is {:f} seconds".format(aggtimeperline[line_no])
    arr.append(varchanges)
    varchanges = "The average time spent on this line till now is {:f} seconds".format(aggtimeperline[line_no]/nooftimesperline[line_no])
    arr.append(varchanges)
    jsndta = {}
    jsndta["timestamp"] = time.time()
    jsndta["report"] = arr
    writetojson.addtolines(jsndta, step)
    

    


stime = time.time()
modle = importlib.import_module(pth)
func = getattr(modle, fname)
sys.settrace(trace_main)
func(3, 5, 0)
sys.settrace(None)

arr = []
for i in answerint:
    arr = []
    strval = "Tracing the variable " + i + " of type integer:-"
    arr.append(strval)
    strval = "It was initialized on line " + str(answerint[i][0])  + "."
    arr.append(strval)
    strval = "It's value over the program ranges from " + str(answerint[i][1]) + " to " + str(answerint[i][1]) + "."
    arr.append(strval)
    lastval = answerint[i][3][0][1]
    strval = "The initial value of the variable is " + str(lastval)  + "."
    arr.append(strval)
    for j in range(1, len(answerint[i][3])):
        strval = "On line "+ str(answerint[i][3][j][0]) + ", the variable changed values from " + str(lastval) + " to " + str(answerint[i][3][j][1]) + "."
        arr.append(strval)
        lastval = answerint[i][3][j][1]
    strval = "The final value of the variable is " + str(lastval)  + "."
    arr.append(strval)
    jsndta = {}
    jsndta["timestamp"] = time.time()
    jsndta["report"] = arr
    writetojson.addtovars(jsndta, i)
    

for i in answerother:
    arr = []
    typevar = str(answerother[i][1])[8:]
    typevar2 = str(typevar[::-1][2:])[::-1]
    strval = "Tracing the variable " + i + " of type %s:-" % (typevar2)
    arr.append(strval)
    strval = "It was initialized on line " + str(answerother[i][0])  + "."
    arr.append(strval)
    lastval = answerother[i][2][0][1]
    strval = "The initial value of the variable is " + str(lastval)  + "."
    arr.append(strval)
    for j in range(1, len(answerother[i][2])):
        strval = "On line "+ str(answerother[i][2][j][0]) + ", the variable changed from " + str(lastval) + " to " + str(answerother[i][2][j][1]) + "."
        arr.append(strval)
        lastval = answerother[i][2][j][1]
    strval = "The final value of the variable is " + str(lastval)  + "."
    arr.append(strval)
    jsndta = {}
    jsndta["timestamp"] = time.time()
    jsndta["report"] = arr
    writetojson.addtovars(jsndta, i)

arr = []
otherdta = "Program executed in {:f} seconds.".format(time.time()-stime)
arr.append(otherdta)
for i in nooftimesperline:
    if( nooftimesperline[i] == 1):
        otherdta = "Line %s was executed %s time" % (i, nooftimesperline[i])
        arr.append(otherdta)
    else: 
        otherdta = "Line %s was executed %s times" % (i, nooftimesperline[i])
        arr.append(otherdta)
jsndta = {}
jsndta["timestamp"] = time.time()
jsndta["report"] = arr
writetojson.addtoothers(jsndta)

writetojson.findata()
writetojson.dumpjson()
print("Written to json file!")