import sys
import copy
variablevalues = {}
answerint = {}
answerother = {}

# answerother[var] = [initialize, type, [[line, change], [line2, change2]]]
# answerint[var] = [initialize, min, max]

def testfunction(a, b):
    test = "sfwef"
    lol = [1,2,3,4,5]
    cnt = {3:4, 5:6}
    a += 1
    b += 5
    lol.append(6)
    lol.append(7)
    lol[3] = 6
    cnt[3] = 7
    lol.remove(5)
    test += "e"
    c = abs(a - b)
    d = a * b * c
    e = a + b + d + c
    test += "gsagar"
    return e



def trace_main(frame, event, args):
    if(event != 'call'):
        return 
    return trace_varchanges

def trace_varchanges(frame, event, args):
    if event != "line":
        return 
    code = frame.f_code
    localvars = frame.f_locals
    for i in code.co_varnames:
        if i in localvars:
            if(isinstance(localvars[i], list)):
                if i not in variablevalues:
                    line_no = frame.f_lineno-1
                    func_name = code.co_name
                    print("In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i]))
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
                                print("In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j]))
                                changed = True
                        for j in range(len(variablevalues[i]), len(localvars[i])):
                            print("In line %s of the %s function in the file %s, the value %s has been added to %s" % (line_no, func_name, code.co_filename, localvars[i][j], i))
                            changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    else:
                        line_no = frame.f_lineno-1
                        func_name = code.co_name
                        for j in range(min(len(variablevalues[i]), len(localvars[i]))):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                print("In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j]))
                                changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    if changed == True:
                        answerother[i][2].append([line_no, variablevalues[i]])
            else:
                if i not in variablevalues:
                    line_no = frame.f_lineno-1
                    func_name = code.co_name
                    print("In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i]))
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
                        print("In line %s of the %s function in the file %s, the variable %s has changed from %s to %s" % (line_no, func_name, code.co_filename, i, variablevalues[i], localvars[i]))
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


sys.settrace(trace_main)
testfunction(3, 4)

print("----------------------------------------------")
print("                     REPORT                   ")
print("----------------------------------------------")
for i in answerint:
    print("Tracing the variable " + i + " of type integer:-")
    print("It was initialized on line " + str(answerint[i][0])  + ".")
    print("It's value over the program ranges from " + str(answerint[i][1]) + " to " + str(answerint[i][1]) + ".")
    lastval = answerint[i][3][0][1]
    print("The initial value of the variable is " + str(lastval)  + ".")
    for j in range(1, len(answerint[i][3])):
        print("On line "+ str(answerint[i][3][j][0]) + ", the variable changed values from " + str(lastval) + " to " + str(answerint[i][3][j][1]) + ".")
        lastval = answerint[i][3][j][1]
    print("The final value of the variable is " + str(lastval)  + ".")
    print("----------------------------------------------")

for i in answerother:
    typevar = str(answerother[i][1])[8:]
    typevar2 = str(typevar[::-1][2:])[::-1]
    print("Tracing the variable " + i + " of type %s:-" % (typevar2))
    print("It was initialized on line " + str(answerother[i][0])  + ".")
    lastval = answerother[i][2][0][1]
    print("The initial value of the variable is " + str(lastval)  + ".")
    for j in range(1, len(answerother[i][2])):
        print("On line "+ str(answerother[i][2][j][0]) + ", the variable changed from " + str(lastval) + " to " + str(answerother[i][2][j][1]) + ".")
        lastval = answerother[i][2][j][1]
    print("The final value of the variable is " + str(lastval)  + ".")
    print("----------------------------------------------")
