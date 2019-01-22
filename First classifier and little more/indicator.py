import numpy as np

def getPeriod(arr, period, pos):
    return arr[pos-period+1:pos+1]

def sma(arr, period, pos):
    return sum([arr[pos-i] for i in range(period)])/period

def rsi(arr, period, start = 0):
    period+=1
    ar = getPeriod(arr,period,start)
    #print(ar)
    tg = 0
    cg = 0
    tl = 0
    cl = 0
    for i in range(1,len(ar)):
        if ar[i]-ar[i-1]>0:
            tg += ar[i]-ar[i-1]
            cg+=1
        else:
            tl += ar[i-1]-ar[i]
            cl+=1

    if cg == 0: return 0
    if cl == 0: return 100

    ag = tg/(period-1)
    al = tl/(period-1)

    rs = ag/al

    #print(ag,al,tg,tl,cg,cl)

    return 100-100/(1+rs)

def momentum(arr, period, curInd):
    return arr[curInd]-arr[curInd-period]

def stoch(close, low, high, period, pos):
    l = getPeriod(low, period, pos)
    h = getPeriod(high, period, pos)

    return 100*(close[pos]-min(l))/(max(h)-min(l))

def sd(arr, period, start = 0):
    ar = np.array(getPeriod(arr, period, start))
    return np.std(ar)

def change(v1,v2):
    return (v2-v1)/v1

def atr(close, high, low, period, ind):
    def tr(ind):
        return max(high[ind]-low[ind], abs(high[ind]-close[ind-1]), abs(low[ind]-close[ind-1]))

    sumTr = 0
    for i in range(period):
        sumTr += tr(ind-i)

    return sumTr/period

def acp(arr, Fast, Slow, ind):
    f = 0
    s = 0
    for i in range(Fast):
        f+=arr[ind-i]
    for i in range(Slow):
        s+=arr[ind-i]
    f/=Fast
    s/=Slow

    return abs(f-s)

def trendDeviation(arr, period, ind):
    _sum = 0
    for i in range(period):
        _sum += arr[ind-i]

    return arr[ind]/_sum
