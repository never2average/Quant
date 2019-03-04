## Core/Support/universes.py

### File Details: This python file contains the Universe class which is used to interact with the list of stock tickers salong with industry stored in the mongodb database.
___

### Dependencies: 
- **Core/Support/config.py**
- **pymongo**
- **quandl**
- **requests**
- **csv**
- **os**
___

### Files used in:
- **Core/Backtest/SENO.py**
- **Core/Backtest/SENQ.py**
- **Core/Support/evaluate.py**
- **Core/Support/dataRegistry.py**
___

## Classes Used:
- **Universe**
___
#### Class Methods:
- **str**
___
#### Instance Methods:
- **routineCheckup**
- **updateUniverses**
- **addUniverse**
- **convertPosts**
- **listUniverseTickers**
___
#### Class Variables:
- **DetailsPath**
##### datatype: String
##### default:getcwd()+"\\objectDetails\\Universe.txt"
___
#### Instance Variables:

- **existingUniverses**
##### datatype:List
##### default:None
___
- **db**
##### datatype:database reference
##### default:None
___
- **client**
##### datatype:MongoClient reference
##### default:None
___
- **dbName**
##### datatype:string
##### default:"universes"
___
- **universes**
##### datatype:string
##### default:"nifty50"
___
- **connectionInfo**
##### datatype:string
##### default:config.defaultConnectionInfo
___
- **isUser**
##### datatype:boolean
##### default:True
___

### Class Methods
    def __str__(self):
        fobj=open(DataRegistry.DetailsPath,"r")
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
def __init__(self,
                 databaseName,
                 universeList,
                 connectionInfo,
                 routineCheckup,
                 isUser)
```
##### Inputs:string,List,string,boolean,boolean
##### Input Defaults: 'universes,list(config.universes.keys()),config.defaultConnectionInfo,True,True
##### Outputs: None
##### Access: public
##### Operation Flow:

```python
try:
    self.universes=universeList
    self.dbName=databaseName
    self.isUser=isUser
    self.connectionInfo=connectionInfo
    if routineCheckup:
        self.routineCheckup()
except:
    return "InputAcceptanceError"
```
___
### Instance Methods
___
    def routineCheckup(self):
        try:
            self.client=pymongo.MongoClient(self.connectionInfo)
            self.db=self.client[self.dbName]
            if not self.isUser:
                self.existingUniverses=self.db.list_collection_names()
                if self.existingUniverses != self.universes:
                    self._updateUniverses()
        except:
            return "RoutineCheckupError"
#### routineCheckup

##### Inputs: None
##### Input Defaults: NA
##### Outputs: String(only in case of error)
##### Access: public
##### Operation: Just a function to perform routine checkup of the universes.Not run normally by user.Only by admin.
___

#### updateUniverses

##### Inputs: None
##### Input Defaults: None
##### Outputs: string
##### Access: private
##### Operation: Checks if the universe database is up to date when compared to the system configurations
___

#### addUniverse

##### Inputs:string
##### Input Defaults: None
##### Outputs: None
##### Access: private
##### Operation: Whenever the variable config.universes changes or the database is corrupted, this method will be executed and the new universes will be added to our current ones.
___

#### convertPosts

##### Inputs: List
##### Input Defaults: None
##### Outputs: List
##### Access: private
##### Operation: converts the input from a 2D List to a List of Dictionaries
___

#### listUniverseTickers

##### Inputs: string
##### Input Defaults: None
##### Outputs: List
##### Access: public
##### Operation:  Lists all the stock tickers in a given universe
___
        