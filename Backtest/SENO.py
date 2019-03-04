# -*- coding: utf-8 -*-

import config
from dataRegistry import DataRegistry
from universe import Universe
from evaluate import CustomInputEvaluator
import pandas as pd
import numpy as np

class SENOBacktest:
    def __init__(self,
                 universeName=config.defaultBacktestUniverse,
                 connectionInfo=config.defaultConnectionInfo,
                 longEntryExpression=config.defaultLongEntryExpression,
                 longExitExpression=config.defaultLongExitExpression,
                 longQuantity=config.defaultLongQuantity,
                 shortEntryExpression=config.defaultShortEntryExpression,
                 shortExitExpression=config.defaultShortExitExpression,
                 shortQuantity=config.defaultShortQuantity,
                 tradingDays=config.defaultTradingDays):
        
        self.connectionInfo=connectionInfo
        
        self.longEntryExpression=longEntryExpression
        self.longExitExpression=longExitExpression
        self.longQuantity=int(longQuantity)
        self.shortEntryExpression=shortEntryExpression
        self.shortExitExpression=shortExitExpression
        self.shortQuantity=int(shortQuantity)
        
        
        self.tradingDays=tradingDays
        self.universeName=universeName
        
        self._initializeUniverseObject()
        if self._isPermissibleTrade():
            self._evaluateSignals()
            self._calculateExposure()
            self._calculatePNL()
            self._calculateGrossPNL()
            
    def _initializeUniverseObject(self):
        self.universeList=Universe(databaseName="universes",
                                   universeList=[self.universeName],
                                   connectionInfo=self.connectionInfo,
                                   routineCheckup=True,
                                   isUser=True).listUniverseTickers(
                                           self.universeName)
        if type(self.universeList)==str:
            self.universeList=self.universeName
            
    def _isPermissibleTrade(self):
        portfolioSize=DataRegistry(connectionInfo=self.connectionInfo)
        portfolioSize.getData("Close",self.universeList)
        portfolioSize=portfolioSize.returnedDF.max().sum()
        portfolioSize*=self.longQuantity+self.shortQuantity
        if portfolioSize>10000000000:
           return False
        self.portfolioSize=(portfolioSize//100+1)*100
        return True
    
    def _singleEvaluateSignals(self,expression):
        anonymousObject=CustomInputEvaluator(rawString=expression,
                                              stockList=self.universeList,
                                              debug=False,
                                              normalizeInput=False,
                                              connectionInfo=self.connectionInfo)
        return anonymousObject.normalizedResult
    
    def _evaluateSignals(self):
        self.longEntrySignals=self._singleEvaluateSignals(
                self.longEntryExpression)
        self.longExitSignals=self._singleEvaluateSignals(
                self.longExitExpression)
        self.shortEntrySignals=self._singleEvaluateSignals(
                self.shortEntryExpression)
        self.shortExitSignals=self._singleEvaluateSignals(
                self.shortEntryExpression)        
        
        del self.longEntryExpression,self.longExitExpression
        del self.shortEntryExpression,self.shortExitExpression
        
    def _calculateExposure(self):
        del self.longEntrySignals,self.longExitSignals
        del self.shortEntrySignals,self.shortExitSignals
    
    def _calculatePNL(self):
        pass
    def _calculateGrossPNL(self):
        pass
        #self.pnl['NetGrossPNL']=self.pnl['GrossLongPNL']+self.pnl['GrossShortPNL']

"""

        for i in range(0,len(EntrySignal)-1):
            exposure.iloc[i+1,0]= int(((EntrySignal.iloc[[i]]&(~ExitSignal.iloc[[i]])) | (EntrySignal.iloc[[i]]&exposure.iloc[i,0]) | ((~ExitSignal.iloc[[i]])&exposure.iloc[i,0])).values)
            exposure2.iloc[i+1,0]= int(((EntrySignal2.iloc[[i]]&(~ExitSignal2.iloc[[i]])) | (EntrySignal2.iloc[[i]]&exposure2.iloc[i,0]) | ((~ExitSignal2.iloc[[i]])&exposure2.iloc[i,0])).values)
        #e(t+1)=b*s^ + be+^S*e

        exposure.iloc[:,0]=exposure.iloc[:,0]*EntryQuantity
        exposure2.iloc[:,0]=exposure2.iloc[:,0]*(-EntryQuantity2)

        #sq
        def pnl(exposure=pd.DataFrame()):

            count=0
            win=0
            loss=0

            for i in range(1,len(exposure)):
                if (exposure.iloc[i,0]==exposure.iloc[i-1,0]):
                    count=count+1
                    if i == len(exposure)-1:
                        exposure.iloc[i,1] = round(float(((c.iloc[[i]] - delay(o, count).iloc[[i]]) * (exposure.iloc[i - 1, 0])).values), 4)
                        exposure.iloc[i, 2] = count
                elif(exposure.iloc[i,0]!=exposure.iloc[i-1,0]):
                    exposure.iloc[i,2]=count
                    exposure.iloc[i,1]=round(float(((o.iloc[[i]]-delay(o,count+1).iloc[[i]])*(exposure.iloc[i-1,0])).values),4)
                    if(exposure.iloc[i,1]>0):
                        win=win+1
                    if(exposure.iloc[i,1]<0):
                        loss=loss+1
                    if( i == len(exposure)-1 and exposure.iloc[i,0]!=0):
                        exposure.iloc[i, 1] = round(float(((c.iloc[[i]] - o.iloc[[i]]) * (exposure.iloc[i, 0])).values), 4)
                        exposure.iloc[i, 2] = count
                    count=0
            return exposure, win, loss

        k1=pnl(exposure)
        k2=pnl(exposure2)

        exposure=k1[0]
        exposure2=k2[0]

        # print(exposure)
        # print("\n"+z+"\n")

        # for i in range(1,len(exposure)):
        #     if(exposure.iloc[i-1,0]==0 and exposure.iloc[i,0]!=0):
        #         print("Enter long position on "+str((exposure.index[[i]]).strftime('%Y-%m-%d')[0])+" Quantity: "+str(exposure.iloc[i,0])+" at "+str(o.iloc[i,0]))
        #     if(exposure.iloc[i-1,0]!=0 and exposure.iloc[i,0]==0):
        #         print("Exit long position on "+str((exposure.index[[i]]).strftime('%Y-%m-%d')[0])+" Quantity: "+str(exposure.iloc[i-1,0])+" at "+str(o.iloc[i,0])+" PNL: "+str(exposure.iloc[i,1])+" in "+str(exposure.iloc[i,2]+1)+" days")
        #     if(exposure2.iloc[i-1,0]==0 and exposure2.iloc[i,0]!=0):
        #         print("Enter short position on "+str((exposure2.index[[i]]).strftime('%Y-%m-%d')[0])+" Quantity: "+str(abs(exposure2.iloc[i,0]))+" at "+str(o.iloc[i,0]))
        #     if(exposure2.iloc[i-1,0]!=0 and exposure2.iloc[i,0]==0):
        #         print("Exit short position on "+str((exposure2.index[[i]]).strftime('%Y-%m-%d')[0])+" Quantity: "+str(abs(exposure2.iloc[i-1,0]))+" at "+str(o.iloc[i,0])+" PNL: "+str(exposure2.iloc[i,1])+" in "+str(exposure2.iloc[i,2]+1)+" days")

        gross_pnl=pd.DataFrame(columns=['PNL'], index=exposure.index)
        gross_pnl.iloc[:,0]=exposure.iloc[:,1].cumsum(axis=0)
        gross_pnl =gross_pnl.fillna(method='ffill')
        gross_pnl2=pd.DataFrame(columns=['PNL'], index=exposure2.index)
        gross_pnl2.iloc[:,0]=exposure2.iloc[:,1].cumsum(axis=0)
        gross_pnl2 =gross_pnl2.fillna(method='ffill')
        net_gross_pnl=gross_pnl+gross_pnl2
"""