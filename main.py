import sys

variablevalues = {}
# really nice task, didnt know you code do all these things with python.
def testfunction(a, b):
    a += 1
    b += 5
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