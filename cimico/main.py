import inspect
import sys
import copy
import time
import timeit
import importlib
import importlib.util
from . import writetojson, outputjson, generatevid, testsuite
# import writetojson
# import outputjson
from inspect import isfunction, getmembers
# import generatevid
# import testsuite

variablevalues = {}
answerint = {}
answerother = {}
aggtimeperline = {}
nooftimesperline = {}

og = sys.stdout
step = 0

def trace_main(frame, event, args):
    if(event != 'call'):
        return 
    return trace_varchanges
lastoutput = []
def trace_varchanges(frame, event, args):
    global step
    global lastoutput
    global og
    if event != "line":
        return
    code = frame.f_code
    localvars = frame.f_locals
    line_no = frame.f_lineno
    arr = []
    strt = "Starting line %s ..." % (line_no)
    arr.append(line_no)
    start_time = time.time()
    step+=1
    vrchngs = []
    vrinitialize = []
    lstchngs = []
    lstadds= []
    lstinitialize = []
    sys.stdout = og
    for i in code.co_varnames:
        if i in localvars:
            if(isinstance(localvars[i], list)):
                if i not in variablevalues:
                    line_no = frame.f_lineno
                    func_name = code.co_name
                    lstinitialize.append([i, localvars[i]])
                    variablevalues[i] = []
                    variablevalues[i] = localvars[i][:]
                    answerother[i] = [line_no, type(localvars[i]), [[line_no, variablevalues[i]]]]
                else:
                    changed = False
                    if (len(variablevalues[i]) < len(localvars[i])):
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        for j in range(len(variablevalues[i])):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                lstchngs.append([i, j, variablevalues[i][j], localvars[i][j]])
                                changed = True
                        for j in range(len(variablevalues[i]), len(localvars[i])):
                            lstadds.append([i, localvars[i][j]])
                            changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    else:
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        for j in range(min(len(variablevalues[i]), len(localvars[i]))):
                            if(variablevalues[i][j] != localvars[i][j]):        
                                lstchngs.append([i, j, variablevalues[i][j], localvars[i][j]])
                                changed = True
                        variablevalues[i] = []
                        variablevalues[i] = localvars[i][:]
                    if changed == True:
                        answerother[i][2].append([line_no, variablevalues[i]])
            else:
                if i not in variablevalues:
                    line_no = frame.f_lineno
                    func_name = code.co_name
                    vrinitialize.append([i, localvars[i]])
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
                        line_no = frame.f_lineno
                        func_name = code.co_name
                        vrchngs.append([i, variablevalues[i], localvars[i]])
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
    line_no = frame.f_lineno
    if line_no not in nooftimesperline:
        nooftimesperline[line_no] = 1
    else:
        nooftimesperline[line_no]+=1
    spent = time.time() - start_time
    if line_no not in aggtimeperline:
        aggtimeperline[line_no] = spent
    else:
        aggtimeperline[line_no]+=spent
    arr.append(spent)
    arr.append(nooftimesperline[line_no])
    arr.append(aggtimeperline[line_no])
    arr.append(aggtimeperline[line_no]/nooftimesperline[line_no])
    arr.append(lstadds)
    arr.append(lstchngs)
    arr.append(lstinitialize)
    arr.append(vrchngs)
    arr.append(vrinitialize)
    file = open("output.txt", "r")
    otpt = ""
    curroutput = list(file.read())
    if(len(lastoutput) < len(curroutput)):
        for i in range(len(lastoutput), len(curroutput)):
            otpt += curroutput[i]
    arr.append(otpt)
    lastoutput = curroutput.copy()
    file.close()
    jsndta = {}
    jsndta["timestamp"] = time.time()
    jsndta["report"] = arr
    writetojson.addtolines(jsndta, step)
    sys.stdout = open("output.txt", "a")
def main():
    print("----------------------------------------------")
    print("                 TAKING INPUT                 ")
    print("----------------------------------------------")
    tests = False
    functest = 0
    a1 = input("Do you want to use the test suite? (y/n): ")
    if a1 == 'y':
        tests = True
        print("Which algorithm do you want to test?")
        print("1 - Quicksort")
        print("2 - Binary Search")
        print("3 - Depth-First Search")
        print("4 - Breadth-First Search")
        print("5 - Knapsack Problem")
        print("6 - Bubble Sort")
        print("7 - Longest Increasing Subsequence")
        print("8 - Longest Common Subsequence")
        print("9 - Insertion Sort")
        print("10 - Kadanes Algorithm")
        t1= int(input("Enter: "))
        while(t1 > 10 or t1<1):
            t1 = int(input("Sorry invalid input! Enter Again:"))
        functest = t1
    else:
        pth2 = input("Enter the name of the file you want to debug: ")
        if pth2.find(".json") != -1:
            inp2 = input("Do you want to generate a video? (y/n): ")
            if(inp2 == 'y'):
                print("Generating video...")
                finpth = generatevid.generatevid(pth2)
                inp3 = input("Do you want to generate a GIF file as well? (y/n)")
                if(inp3 == "y"):
                    print("Generating GIF...")
                    generatevid.convertogif(finpth)
                exit()
            print("You entered a JSON file, reporting the data...")
            outputjson.output(pth2)
            exit()
        if pth2.find(".py") == -1:
            print("Invalid file, breaking the program")
            exit()
        fname = input("Enter the name of the function you want to debug: ")
        pth = pth2.replace(".py", "")
        spec = importlib.util.spec_from_file_location("func", pth2)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        if(not hasattr(foo, fname)):
            print("Invalid input! Either wrong function name or wrong path!")
            exit()
    args = list(input("Enter the arguments for the function (space seperated): ").split())
    for i in range(len(args)):
        args[i] = int(args[i])
    print("----------------------------------------------")
    print("              RUNNING FUNCTION                ")
    print("----------------------------------------------")


    stime = time.time()
    if(tests == False):
        spec = importlib.util.spec_from_file_location("func", pth2)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        func = getattr(foo, fname)
        writetojson.addtosource(inspect.getsource(func))
    else:
        testsuite.initiliazegraph()
        if functest== 1:
            testsuite.quicksort([4, 8, 5, 6, 2, 10])
            writetojson.addtosource(inspect.getsource(testsuite.quicksort))
        elif functest==2:
            writetojson.addtosource(inspect.getsource(testsuite.binarysearch))
        elif functest==3:
            writetojson.addtosource(inspect.getsource(testsuite.dfs))
        elif functest==4:
            writetojson.addtosource(inspect.getsource(testsuite.bfs))
        elif functest==5:
            writetojson.addtosource(inspect.getsource(testsuite.knapsack))
        elif functest==6:
            writetojson.addtosource(inspect.getsource(testsuite.bubblesort))
        elif functest==7:
            writetojson.addtosource(inspect.getsource(testsuite.lis))
        elif functest==8:
            writetojson.addtosource(inspect.getsource(testsuite.lcs))
        elif functest==9:
            writetojson.addtosource(inspect.getsource(testsuite.insertionsort))
        elif functest==10:
            writetojson.addtosource(inspect.getsource(testsuite.kadanes))
    sys.stdout = open("output.txt", "w")
    sys.settrace(trace_main)
    if(tests == True):
        if functest== 1:
            testsuite.quicksort([4, 8, 5, 6, 2, 10])
        elif functest==2:
            testsuite.binarysearch([2, 6, 9, 10, 14], 0, 4, 6)
        elif functest==3:
            testsuite.dfs(testsuite.adj, testsuite.visited, 1)
        elif functest==4:
            testsuite.bfs(testsuite.adj, testsuite.visited, 1)
        elif functest==5:
            testsuite.knapsack(50, [10,20,30], [60,100,120], 3)
        elif functest==6:
            testsuite.bubblesort([4, 8, 5, 6, 2, 10])
        elif functest==7:
            testsuite.lis([4, 8, 5, 6, 2, 10])
        elif functest==8:
            testsuite.lcs("AGGTAB", "GXTXAYB", 6, 7)
        elif functest==9:
            testsuite.insertionsort([4, 8, 5, 6, 2, 10])
        elif functest==10:
            testsuite.kadanes([-2, -3, 4, -1, -2, 1, 5, -3])
    else:
        func(*args)

    sys.settrace(None)
    sys.stdout = og
    arr = []
    for i in answerint:
        arr = []
        arr.append(i)
        arr.append(answerint[i][0])
        lastval = answerint[i][3][0][1]
        arr.append(lastval)
        arr2 = []
        for j in range(1, len(answerint[i][3])):
            arr2.append([answerint[i][3][j][0], lastval, answerint[i][3][j][1]])
            lastval = answerint[i][3][j][1]
        arr.append(arr2)
        jsndta = {}
        jsndta["timestamp"] = time.time()
        jsndta["report"] = arr
        jsndta["ifint"] = True
        jsndta["type"] = "int"
        writetojson.addtovars(jsndta, i)
        
    for i in answerother:
        arr = []
        typevar = str(answerother[i][1])[8:]
        typevar2 = str(typevar[::-1][2:])[::-1]
        arr.append(i)
        arr.append(answerother[i][0])
        lastval = answerother[i][2][0][1]
        arr.append(lastval)
        arr2 = []
        for j in range(1, len(answerother[i][2])):
            arr2.append([answerother[i][2][j][0], lastval, answerother[i][2][j][1]])
            lastval = answerother[i][2][j][1]
        arr.append(arr2)
        jsndta = {}
        jsndta["timestamp"] = time.time()
        jsndta["report"] = arr
        jsndta["type"] = typevar2
        writetojson.addtovars(jsndta, i)

    arr = []
    arr.append(time.time()-stime)
    for i in nooftimesperline:
        arr.append([i, nooftimesperline[i]])
    jsndta = {}
    jsndta["timestamp"] = time.time()
    jsndta["report"] = arr
    writetojson.addtoothers(jsndta)
    writetojson.findata()
    pthtojson = input("Where do you want your JSON file to be stored? ")
    writetojson.dumpjson(pthtojson)
    print("Written to json file!")

