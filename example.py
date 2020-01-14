def main(y, x, a):
    x += y
    y += x
    z = x * y
    return x + y + z


def testfunction(a, b, curr):
    if(curr == 3):
        return a+b
    curr+=1
    test = "sfwef"
    a += 1
    b += 5
    n = 0
    while n<10:
        n+=1
    test += "e"
    c = abs(a - b)
    d = a * b * c
    e = a + b + d + c
    test += "gsagar"
    return e + testfunction(d, e, curr)
