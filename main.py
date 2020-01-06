import sys

variablevalues = {}

def testfunction(a, b):
    lol = [1,2,3,4,5]
    a += 1
    b += 5
    lol.append(6)
    lol.append(7)
    c = abs(a - b)
    d = a * b * c
    e = a + b + d + c
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
            if(isinstance(i, list)):
                if i not in variablevalues:
                    line_no = frame.f_lineno
                    func_name = code.co_name
                    if(func_name == 'testfunction'):
                        print("In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i]))
                    variablevalues[i] = localvars[i]
                else:
                    if (len(variablevalues[i]) < len(localvars[i])):
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        for j in range(len(variablevalues[i])):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                if(func_name == 'testfunction'):
                                    print("In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j]))
                        for j in range(len(variablevalues[i]), len(localvars[i])):
                            if(func_name == 'testfunction'):
                                    print("In line %s of the %s function in the file %s, %s has been added to %s" % (line_no, func_name, code.co_filename, localvars[i][j], i))
                        variablevalues[i] = localvars[i]
                    else:
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        for j in range(min(len(variablevalues[i]), localvars[i])):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                if(func_name == 'testfunction'):
                                    print("In line %s of the %s function in the file %s, the index %s of list %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, j, i, variablevalues[i][j], localvars[i][j]))
                        variablevalues[i] = localvars[i]
            else:
                if i not in variablevalues:
                    line_no = frame.f_lineno
                    func_name = code.co_name
                    if(func_name == 'testfunction'):
                        print("In line %s of the %s function in the file %s, the variable %s has been initialized to %s" % (line_no, func_name, code.co_filename,i, localvars[i]))
                    variablevalues[i] = localvars[i]

                else:
                    if(localvars[i] != variablevalues[i]):
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        if(func_name == 'testfunction'):
                            print("In line %s of the %s function in the file %s, the variable %s has changed value from %s to %s" % (line_no, func_name, code.co_filename, i, variablevalues[i], localvars[i]))
                        variablevalues[i] = localvars[i]


sys.settrace(trace_main)
testfunction(3, 4)