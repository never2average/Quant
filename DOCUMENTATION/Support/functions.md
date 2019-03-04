# Core/Support/functions.py


### File Details: This python file contains the list of all proprietary functions that are required for analysis in the SENO and SENQ back test modules

___
### Dependencies: pandas, talib
___

### Files used in:
- **Core/Support/config.py**
___
## Function Names:
- **SMA**
- **EMA**
- **csRank**
- **csMean**
- **tsRank**
- **Sum**
- **tsMax**
- **csMax**
- **tsMin**
- **csMin**
- **stdDev**
- **tsZscore**
- **delay**
- **delta**
- **momentum**
-  **RSI**

___

SMA
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates the simple moving average of an attribute over the last k days
___

EMA
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates the exponentially weighted average of an attribute over the last k days
___

csRank
------
### Inputs: Dataframe 
### Input Defaults: pd.DataFrame() 
### Outputs: Dataframe
### Access: package-private
### Operations: Ranks the given attribute row wise
___

csMean
------
### Inputs: Dataframe 
### Input Defaults: pd.DataFrame() 
### Outputs: Dataframe
### Access: package-private
### Operations: calculates cross sectional mean of given attribute (row wise mean)
___

tsRank
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: 
___

Sum
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: 
___

tsMax
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates column wise maximum value of attribute over rolling window k
___

csMax
------
### Inputs: Dataframe 
### Input Defaults: pd.DataFrame() 
### Outputs: Dataframe
### Access: package-private
### Operations: 
___

tsMin
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates column wise minimum value of attribute over rolling window k
___

csMin
------
### Inputs: Dataframe 
### Input Defaults: pd.DataFrame() 
### Outputs: Dataframe
### Access: package-private
### Operations: 
___

stdDev
------
### Inputs: Dataframe , Integer, Integer
### Input Defaults: pd.DataFrame() , 30, 1
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates column wise standard deviation of attribute over rolling window k
___

tsZscore
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates column wise z-score value (x-mean/stddex(x)) of attribute over rolling window k
___

delay
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Shifts data available forward by k periods. This means today you have access <br> to data that is at least k days old
___

delta
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations:  Measures the change in the value of an attribute over the past k days.
___

momentum
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates the momentum of a given attribute over a k day time-period
___

RSI
------
### Inputs: Dataframe , Integer
### Input Defaults: pd.DataFrame() , 30
### Outputs: Dataframe
### Access: package-private
### Operations: Calculates the relative strength index of a given attribute over a k day time-period
___

### Note: Whenever you would like to make a new function available for public use, do the following
- **Copy the function definition to this file**
- **Insert into the availableFunctions dictionary <br>
of Core/Support/config.py file as &lt; method public string &gt; : config.methodName**
____
