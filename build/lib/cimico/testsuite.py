adj= {}
visited = []

def initiliazegraph():
    n = 8
    for i in range(0, n+1):
        visited.append(False)
        adj[i] = []
    adj[1].append(2)
    adj[1].append(4)
    adj[4].append(3)
    adj[4].append(5)
    adj[2].append(1)
    adj[4].append(1)
    adj[3].append(4)
    adj[5].append(4)
    adj[6].append(7)
    adj[7].append(8)
    adj[7].append(6)
    adj[8].append(7)
    adj[2].append(6)
    adj[6].append(2)
    

def quicksort(arr):
    l = []
    equal = []
    r = []
    if len(arr) > 1:
        pvt = arr[0]
        for x in arr:
            if x < pvt:
                l.append(x)
            elif x == pvt:
                equal.append(x)
            elif x > pvt:
                r.append(x)
        arr = quicksort(l)+equal+quicksort(r)
        return arr
    else:
        return arr

def binarysearch(arr, l, r, x):
    if r >= l: 
        mid = int(l + (r - l)/2)
        if arr[mid] == x: 
            return mid 
        elif arr[mid] > x: 
            return binarysearch(arr, l, mid-1, x) 
        else: 
            return binarysearch(arr, mid+1, r, x) 
    else: 
        return -1

def dfs(adj, visited, s):
    visited[s] = True
    for u in adj[s]:
        if not visited[u]:
            dfs(adj, visited, u)

def bfs(adj, visited, s):
    q = []
    q.append(s)
    while len(q) != 0:
        u = q[0]
        visited[u]= True
        q.pop(0)
        for v in adj[u]:
            if not visited[v]:
                q.append(v)

def knapsack(left, wt, val, n):
    if n == 0 or left == 0 : 
        return 0
    if (wt[n-1] > left): 
        return knapsack(left, wt, val, n-1) 
    else: 
        return max(val[n-1] + knapsack(left-wt[n-1], wt, val, n-1), knapsack(left, wt, val, n-1)) 

def bubblesort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def lis(arr):
    dp = []
    for i in range(len(arr)):
        dp.append(i)
    for i in range(len(arr)):
        for j in range(0, i):
            if(arr[j] < arr[i] and dp[i] < dp[j]+1):
                dp[i] = dp[j]+1
    ans =1 
    for i in dp:
        ans= max(i, ans)
    return ans

def lcs(s, t, n, m):
    if m == 0 or n == 0: 
       return 0
    elif t[m-1] == s[n-1]: 
       return 1 + lcs(s, t, n-1, m-1)
    else: 
       return max(lcs(s, t, n, m-1), lcs(s, t, n-1, m))

def insertionsort(arr):
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >= 0 and key < arr[j]: 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 
    return arr

def kadanes(arr):
    curr = 0
    maxans = 0
    for i in range(len(arr)):
        curr += arr[i]
        curr = max(curr, 0)
        maxans = max(curr, maxans)
    return maxans