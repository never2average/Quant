## Core/Support/evaluate.py

### File Details: This python file contains the CustominputEvaluator class which is used to evaluate string inputs that are entered in the SENO and SENQ
___

### Dependencies: 
- **Core/Support/universe.py**
- **Core/Support/dataRegistry.py**
- **Core/Support/config.py**
- **keyword**
- **numpy**
- **os**
___

### Files used in:
- **Core/Backtest/SENO.py**
- **Core/Backtest/SENQ.py**
___

## Classes Used:
- **CustomInputEvaluator**
___
#### Class Methods:
- str
___
#### Instance Methods:
- **computeAlphaAndNormalize**
- **normalize**
- **usedKeywords**
- **everythingExists**
- **loadDFs**
___
#### Class Variables:
- **DetailsPath**
##### datatype: String
##### default:getcwd()+"\\objectDetails\\CustomInputEvaluator.txt"
___
#### Instance Variables:

- **dfList**
##### datatype:List
##### default:[]
___
- **dfDict**
##### datatype:Dictionary
##### default:{}
___
- **stockList**
##### datatype:List
##### default:["ITC","TITAN"]
___
- **rawString**
##### datatype:string
##### default:"Close-Open"
___
- **evaluatableString**
##### datatype:string
##### default:"Close-Open"
___
- **connectionInfo**
##### datatype:string
##### default:config.defaultConnectionInfo
___
- **normalizedResult**
##### datatype:pandas dataframe
##### default:None
___
- **debug**
##### datatype:boolean
##### default:config.debug
___
- **result**
##### datatype:pandas dataframe
##### default:None
___
### Class Methods
    def __str__(self):
        fobj=open(CustomInputEvaluator.DetailsPath,"r")
        details=fobj.read()
        fobj.close()
        return details
##### Inputs: None
##### Input Defaults:NA
##### Outputs: string
##### Access: public
___
### Constructor

```python
def __init__(self, rawString, stockList,debug,connectionInfo,normalizeInput)
```

##### Inputs: string,List,boolean,string,boolean
##### Input Defaults: "Close-Open",["ITC","TITAN"],config.debug,config.defaultConnectionInfo,True
##### Outputs: None
##### Access: public
##### Operation Flow:

```python
if not self._usedKeywords():
	if self._everythingExists():
		self._loadDFs()
		self._computeAlphaAndNormalize(normalizeInput)
```
___
### Instance Methods
___
#### usedKeywords

##### Inputs: None
##### Input Defaults: NA
##### Outputs: Boolean
##### Access: private
##### Operation: Checks if a given alpha expression contains python keywords.Used only for security to prevent injections. 
___

#### everythingExists

##### Inputs: None
##### Input Defaults: NA
##### Outputs: Boolean
##### Access: private
##### Operation: Checks if a given alpha expression contains valid syntax or not.
___

#### loadDFs

##### Inputs: None
##### Input Defaults: NA
##### Outputs: None
##### Access: private
##### Operation: Loads the dataframes that the given in dfList from the database and fills it into the dfDict.
___

#### normalize

##### Inputs: None
##### Input Defaults: NA
##### Outputs: NA
##### Access: private
##### Operation: Normalizes the result dataframe, when called
___

#### computeAlphaAndNormalize

##### Inputs: normalizeInput
##### Input Defaults: True
##### Outputs: NA
##### Access: private
##### Operation: Evaluates the given alpha expression, given it is is correct syntactialy and does not use any keywords. If normalizeInput is True, then it normalizes the result also.
___