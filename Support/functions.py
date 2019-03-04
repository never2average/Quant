# -*- coding: utf-8 -*-

import pandas as pd
import talib as tb

def SMA(x=pd.DataFrame(),k=30):
    y=pd.DataFrame(columns = x.columns)
    for i in range(0,len(x.columns)):
        y.iloc[:,i]=pd.Series(tb.SMA((x.iloc[:,i]).values,timeperiod=k))
    y2=y.set_index(x.index)
    return y2

def EMA(x=pd.DataFrame(),k=30):
    y=pd.DataFrame(columns = x.columns)
    for i in range(0,len(x.columns)):
        y.iloc[:,i]=pd.Series(tb.EMA((x.iloc[:,i]).values,timeperiod=k))
    y2=y.set_index(x.index)
    return y2

def csRank(x=pd.DataFrame()):
    y2=x.rank(axis=1,pct=True)
    return y2

def csMean(x=pd.DataFrame()):
    y=pd.DataFrame(columns=x.columns,index=x.index)
    for i in range(len(x.columns)):
        y.iloc[:,i]=x.mean(axis=1)
    return y

def tsRank(x=pd.DataFrame(),k=30):
    y2=pd.DataFrame(index=x.index,columns=x.columns)
    for i in range(k,len(x)+1):
        y=(x.iloc[i-k:i,:]).rank(axis=0,pct=True)
        y2.iloc[i-1,:]=y.iloc[-1,:]
    return y2

def Sum(x=pd.DataFrame(),k=30):
    y2=pd.DataFrame(index=x.index,columns=x.columns)
    for i in range(k,len(x)+1):
        y=(x.iloc[i-k:i,:]).sum(axis=0)
        y2.iloc[i-1,:]=y
    return y2

def tsMax(x=pd.DataFrame(),k=30):
    y2=pd.DataFrame(index=x.index,columns=x.columns)
    for i in range(k,len(x)+1):
        y=(x.iloc[i-k:i,:]).max(axis=0)
        y2.iloc[i-1,:]=y
    return y2

def csMax(x=pd.DataFrame()):
    y=pd.DataFrame(columns=x.columns,index=x.index)
    for i in range(len(x.columns)):
        y.iloc[:,i]=x.max(axis=1)
    return y

def tsMin(x=pd.DataFrame(),k=30):
    y2=pd.DataFrame(index=x.index,columns=x.columns)
    for i in range(k,len(x)+1):
        y=(x.iloc[i-k:i,:]).min(axis=0)
        y2.iloc[i-1,:]=y
    return y2

def csMin(x=pd.DataFrame()):
    y=pd.DataFrame(columns=x.columns,index=x.index)
    for i in range(len(x.columns)):
        y.iloc[:,i]=x.min(axis=1)
    return y

def stdDev(x=pd.DataFrame(),k=30):
    y=pd.DataFrame(columns = x.columns)
    for i in range(0,len(x.columns)):
        y.iloc[:,i]=pd.Series(tb.STDDEV((x.iloc[:,i]).values,timeperiod=k))
    y2=y.set_index(x.index)
    return y2

def tsZscore(x=pd.DataFrame(),k=30):
    y = pd.DataFrame(columns=x.columns, index=x.index)
    y = (x-SMA(x,k))/stdDev(x,k)
    return y

def delay(x=pd.DataFrame(),k=30):
    y=x.shift(periods=k)
    return y

def delta(x=pd.DataFrame(),k=30):
    y=x-delay(x,k)
    return y

def momentum(x=pd.DataFrame(),k=30):
    y=pd.DataFrame(columns = x.columns)
    for i in range(0,len(x.columns)):
        y.iloc[:,i]=pd.Series(tb.MOM((x.iloc[:,i]).values,timeperiod=k))
    y2=y.set_index(x.index)
    return y2

def RSI(x=pd.DataFrame(),k=30):
    y=pd.DataFrame(columns = x.columns)
    for i in range(0,len(x.columns)):
        y.iloc[:,i]=pd.Series(tb.RSI((x.iloc[:,i]).values,timeperiod=k))
    y2=y.set_index(x.index)
    return y2
