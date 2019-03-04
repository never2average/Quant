# -*- coding: utf-8 -*-

from universe import Universe
from dataRegistry import DataRegistry
import config
import keyword
import numpy as np
from os import getcwd


class CustomInputEvaluator:

    DetailsPath=getcwd()+"\\objectDetails\\CustomInputEvaluator.txt"
    def __str__(self):
        fobj=open(CustomInputEvaluator.DetailsPath,"r")
        details=fobj.read()
        fobj.close()
        return details

    def __init__(self,
                 rawString="Close-Open",
                 stockList=["ITC","TITAN"],
                 debug=config.debug,
                 connectionInfo=config.defaultConnectionInfo,
                 normalizeInput=True):

        self.debug=debug
        self.rawString=rawString
        self.stockList=stockList
        self.evaluatableString=rawString
        self.connectionInfo=connectionInfo

        self.dfList=[]
        self.dfDict={}
        if not self._usedKeywords():
            if self._everythingExists():
                self._loadDFs()
                self._computeAlphaAndNormalize(normalizeInput)

    def _computeAlphaAndNormalize(self,normalizeInput):
        try:
            if self.debug:
                print("Computing alpha expression.")
            try:
                self.result=eval(self.evaluatableString)
                self.result=self.dfDict["Close"]
                self.result.iloc[:,:]=1
            except:
                self.result=eval(self.evaluatableString,
                                 self.dfDict,
                                 config.availableFunctions)
            if self.debug:
                print("Alpha expression successfully computed")

            if normalizeInput:
                self._normalize()
            else:
                self.normalizedResult=self.result
                del self.result
        except SyntaxError as e:
            print(e)

    def _normalize(self):

        if self.debug:
            print("Normalizing alpha values")

        normalizationRatio=np.absolute(self.result).sum(axis=1)[:,None]
        self.normalizedResult=np.divide(self.result,normalizationRatio)

        if self.debug:
            print("Alpha values have been normalized")

    def _usedKeywords(self):
        if self.debug:
            print("Checking for keywords in input expression")

        self.rawString="".join((char if char.isalnum() else " ") for char in
                               self.rawString).split()
        for word in self.rawString:
            if word in keyword.kwlist:
                if self.debug:
                    print("Checked for keywords in expression.Found One word:"+word)
                return True
        if self.debug:
            print("Checked for keywords in expression.Found None.")
        return False


    def _everythingExists(self):
        n=0
        if self.debug:
            print("Checking if syntax is valid")
        for word in self.rawString:
            if word.isdigit():
                n+=1
            elif word.capitalize() in list(config.dataRegistries.keys()):
                self.dfList.append(word.capitalize())
                n+=1
            elif word in config.availableFunctions.keys():
                n+=1
        if n==len(self.rawString):
            if self.debug:
                print("Checks Completed.Syntax is valid.")
            return True
        else:
            if self.debug:
                print("Checks Completed. Encountered invalid syntax.")
            return False

    def _loadDFs(self):
        if self.debug:
            print("Beginning to load dataframes")

        anonymousObject=DataRegistry(startDate='2008-05-31'
                                     ,endDate='2018-05-31'
                                     ,eqList=Universe(databaseName="universes",
                                                     universeList=['nifty500'],
                                                     connectionInfo=self.connectionInfo,
                                                     routineCheckup=True,
                                                     isUser=True
                                             ).listUniverseTickers('nifty500')
                                     ,dataSource="quandl"
                                     ,databaseName="{}_data_registry".format(
                                             config.universes['nifty500'])
                                     ,registryList=list(config.dataRegistries.keys())
                                     ,connectionInfo=self.connectionInfo)

        anonymousObject.getData("Close",self.stockList)

        self.dfDict["Close"]=anonymousObject.returnedDF

        for word in self.dfList:
            anonymousObject.getData(word,self.stockList)
            self.dfDict[word]=anonymousObject.returnedDF

        if self.debug:
            print("Completed loading all necessary dataframes")
            print(self.dfDict["Close"].head(1))
