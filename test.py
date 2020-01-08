from inspect import signature
import importlib

def foo(a, b, c):
    return a+b+c

modle = importlib.import_module("example")
func = getattr(modle, "testfunction")

sig = signature(func)
print(sig)