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
    return e + testfunction(d, e, curr)

