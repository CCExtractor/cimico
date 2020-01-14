import inspect 
import example
import testsuite
import writetojson
import importlib

def lmao():
    return 0

modle = importlib.import_module('example')
func = getattr(modle, 'main')

print(inspect.getsource(func))