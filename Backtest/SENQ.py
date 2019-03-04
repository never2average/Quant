# -*- coding: utf-8 -*-
import sys
sys.path.append('../Support')
from universe import Universe
import config
from os import getcwd
from evaluate import CustomInputEvaluator
import pandas as pd
import numpy as np

def rollingSharpe(y=pd.DataFrame()):
    return np.sqrt(252) * (y.mean() / y.std())

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
        self._generateLog()
        self._generateVolatility()
        self._generateYearlyReturns()
        self._generateSharpe()
        self._generateTurnover()
        self._generateMaximumDrawdown()
        
    def _generatePNL(self):

        self.pnl=self.amountPurchasedTotal*self.closeChange.shift(1)
        self.pnl.dropna(inplace=True)
        self.pnl=self.pnl.round(2)
        self.pnl["DailyPortfolioPnL"]=self.pnl.sum(axis=1)
        self.pnl["Returns"]=self.pnl["DailyPortfolioPnL"]*100/self.portfolioSize
        self.pnl["GrossPortfolioPnL"]=self.pnl["DailyPortfolioPnL"].cumsum()

    def _generateYearlyReturns(self):

        self.yearlyReturns=self.pnl["DailyPortfolioPnL"].groupby(
                self.pnl["DailyPortfolioPnL"].index.year).sum()
        self.yearlyReturns=self.yearlyReturns*100/self.portfolioSize

        self.yearlyReturns.columns=['Yearly Returns']
        self.yearlyReturns=self.yearlyReturns.round(2)
        self.yearlyReturns.index.names=["Year"]

    def _generateSharpe(self):
        self.rollingSharpeRatio=self.pnl['Returns'].rolling('252d').apply(rollingSharpe).dropna()
        self.rollingSharpeRatio.columns=['Rolling Sharpe']
        self.rollingSharpeRatio=self.rollingSharpeRatio.round(2)
        self.rollingSharpeRatio.index.names=["Date"]
        self.rollingSharpeRatio.to_csv(getcwd()+"\TestResult\rolling_sharpe.csv")
        
    def _generateTurnover(self):

        self.turnover=self.alpha.rolling('252d').diff().abs().sum(axis=1).dropna().mean()
        self.turnover.columns=['Rolling Turnover']
        self.turnover=self.turnover.round(2)
        self.turnover.index.names=["Year"]
        self.rollingSharpeRatio.to_csv(getcwd()+"\TestResult\rolling_turnover.csv")

    def _generateMaximumDrawdown(self):
        self.rollingMaxDrawdown=self.pnl["DailyPortfolioPnL"].cummax(
                )-self.pnl["DailyPortfolioPnL"]

        self.rollingMaxDrawdown.columns=['Maximum Drawdown']
        self.rollingMaxDrawdown=self.maxDrawdown.round(2)
        self.rollingMaxDrawdown.index.names=["Year"]
        self.rollingMaxDrawdown.to_csv(getcwd()+"\TestResult\rolling_drawdown.csv")

    def _generateVolatility(self):
        self.volatility=self.pnl["DailyPortfolioPnL"].rolling('252d').std()
        self.volatility.columns=['Rolling Volatility']
        self.volatility=self.volatility.round(2)
        self.volatility.index.names=["Year"]
        self.volatility.to_csv(getcwd()+"\TestResult\rolling_volatility.csv")

    def _generateLog(self,dataframe):
        logDataframe=pd.DataFrame()
        dataframe.drop(["DailyPortfolioPnL","GrossPortfolioPnL"],axis=1,inplace=True)
        logDataframe.index=dataframe.index
        logDataframe["Max"]=dataframe.idxmax(axis=1)
        logDataframe["Min"]=dataframe.idxmax(axis=1)
        logDataframe["Hit Ratio"]=dataframe.select_dtypes(include='float64').gt(0).sum(axis=1)/dataframe.select_dtypes(include='float64').lt(0).sum(axis=1)
        logDataframe.to_csv(getcwd()+"\TestResult\log.csv")