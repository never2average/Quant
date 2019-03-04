#API key for using the quandl API
quandlKey="PcpVUJzsozvy6Xs4BCxo"

#List of Currently Available Data Registries for analysis
dataRegistries={'Open':1, 'High':2,
                'Low':3, 'Last':4,
                'Close':5,'Volume':6
                ,'Turnover':7}

#List of universes/sub-universes available for analysis along with respective 
#stock exchange

universes={"nifty50":'nse',
           "niftynext50":'nse',
           "nifty100":'nse',
           "nifty200":'nse',
           "nifty500":'nse'}

#Base Url for extracting the list of stocks on a particular stock exchange
urlBase={'nse':"https://www.nseindia.com/content/indices/ind_{}list.csv",
         }

#Default connection information for the mongodb database 
defaultConnectionInfo="mongodb://localhost:27017/"

#Dictionary containing the list of available functions for analysis
import functions
availableFunctions={"SMA":functions.SMA,
                    "EMA":functions.EMA,
                    "csRank":functions.csRank,
                    "csMean":functions.csMean,
                    "tsRank":functions.tsRank,
                    "Sum":functions.Sum,
                    "tsMax":functions.tsMax,
                    "csMax":functions.csMax,
                    "tsMin":functions.tsMin,
                    "csMin":functions.csMin,
                    "stdDev":functions.stdDev,
                    "tsZscore":functions.tsZscore,
                    "delay":functions.delay,
                    "delta":functions.delta,
                    "momentum":functions.momentum,
                    "RSI":functions.RSI}

#Default information for CustomInputEvaluator class
debug=False

#Default Information for the SENQ backtesting platform
defaultBacktestUniverse="nifty50"
defaultAlphaExpression="Close-SMA(Close)"
defaultPortfolioSize=1000000
defaultTradingDays=250

#Default Information for the SENO backtesting platform
defaultLongEntryExpression="Close>Open"
defaultLongSellExpression="Low<SMA(Low)"
defaultLongQuantity="10"
defaultShortEntryExpression="High>SMA(High)"
defaultShortSellExpression="RSI(Close,14)>70"
defaultShortQuantity="5"