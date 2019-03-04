# -*- coding: utf-8 -*-

from universe import Universe
import config
from evaluate import CustomInputEvaluator
import pandas as pd
import numpy as np

class SENQBacktest:
    
    def __init__(self,
                 universeName=config.defaultBacktestUniverse,
                 connectionInfo=config.defaultConnectionInfo,
                 alphaExpression=config.defaultAlphaExpression,
                 portfolioSize=config.defaultPortfolioSize,
                 tradingDays=config.defaultTradingDays):
        
        self.connectionInfo=connectionInfo
        self.alphaExpression=alphaExpression
        self.portfolioSize=portfolioSize
        self.tradingDays=tradingDays
        self.universeName=universeName
        
        self._initializeUniverseObject()
        self._evaluateAlpha()
        self._performBacktest()
        self._calculateStatistics()
        
    def _initializeUniverseObject(self):
        self.universeList=Universe(databaseName="universes",
                                   universeList=[self.universeName],
                                   connectionInfo=self.connectionInfo,
                                   routineCheckup=True,
                                   isUser=True).listUniverseTickers(
                                           self.universeName)
    
    def _evaluateAlpha(self):
        evaluationObject=CustomInputEvaluator(rawString=self.alphaExpression,
                                              stockList=self.universeList,
                                              debug=False,
                                              connectionInfo=self.connectionInfo)
        
        self.alpha=evaluationObject.normalizedResult
        self.closeDF=evaluationObject.dfDict["Close"]
        self.alpha.index = pd.to_datetime(self.alpha.index)
        
    def _performBacktest(self):
        
        self.amountPurchasedTotal=self.alpha*self.portfolioSize
        self.amountPurchasedTotal/=self.closeDF
        self.amountPurchasedTotal=self.amountPurchasedTotal.apply(np.floor)
        self.closeChange=self.closeDF.diff().fillna(0)
    
    def _calculateStatistics(self):

        self._generatePNL()
        self._generateYearlyReturns()
        self._generateIR()
        self._generateSharpe()
        self._generateTurnover()
        self._generateMaximumDrawdown()
        self._generateFitness()
        
    def _generatePNL(self):
        
        self.pnl=self.amountPurchasedTotal*self.closeChange.shift(1)
        self.pnl.dropna(inplace=True)
        self.pnl=self.pnl.round(2)    
        self.pnl["DailyPortfolioPnL"]=self.pnl.sum(axis=1)    
        self.pnl["GrossPortfolioPnL"]=self.pnl["DailyPortfolioPnL"].cumsum()
        
    def _generateYearlyReturns(self):
        
        self.yearlyReturns=self.pnl["DailyPortfolioPnL"].groupby(
                self.pnl["DailyPortfolioPnL"].index.year).sum()
        self.yearlyReturns=self.yearlyReturns*100/self.portfolioSize
        
        self.yearlyReturns.columns=['Yearly Returns']
        self.yearlyReturns=self.yearlyReturns.round(2)
        self.yearlyReturns.index.names=["Year"]
        
    def _generateIR(self):
        
        self.informationRatio=self.yearlyReturns*self.portfolioSize/(100*self.tradingDays)
        self.informationRatio=self.informationRatio/self.pnl[
                "DailyPortfolioPnL"].groupby(
                self.pnl["DailyPortfolioPnL"].index.year).std()
        
        self.informationRatio.columns=['Information Ratio']
        self.informationRatio=self.informationRatio.round(2)
        self.informationRatio.index.names=["Year"]
        
    def _generateSharpe(self):
        
        self.sharpeRatio=self.informationRatio*np.sqrt(self.tradingDays)
        
        self.sharpeRatio.columns=['Sharpe Ratio']
        self.sharpeRatio=self.sharpeRatio.round(2)
        self.sharpeRatio.index.names=["Year"]
        
    def _generateTurnover(self):
        
        self.turnover=self.alpha.diff().dropna().abs().sum(axis=1)
        self.turnover=self.turnover.groupby(
                self.turnover.index.year).mean()
        
        self.turnover.columns=['Turnover']
        self.turnover=self.turnover.round(2)
        self.turnover.index.names=["Year"]
        
    def _generateMaximumDrawdown(self):
        self.maxDrawdown=self.pnl["DailyPortfolioPnL"].cummax(
                )-self.pnl["DailyPortfolioPnL"]
        
        self.maxDrawdown=self.maxDrawdown.groupby(
                self.maxDrawdown.index.year).min()
        
        self.maxDrawdown.columns=['Maximum Drawdown']
        self.maxDrawdown=self.maxDrawdown.round(2)
        self.maxDrawdown.index.names=["Year"]
    
    def _generateFitness(self):
        self.fitness=np.sign(self.yearlyReturns)*self.sharpeRatio.abs()*(
                (self.yearlyReturns.abs()/self.turnover)**0.5)
        
        self.fitness.columns=['Fitness']
        self.fitness=self.fitness.round(2)
        self.fitness.index.names=["Year"]