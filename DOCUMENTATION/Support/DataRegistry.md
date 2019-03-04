## Core/Support/dataRegistry.py

### File Details: This python file contains the DataRegistry class which is used to interact with the data registries in the mongodb databases.
___

### Dependencies: 
- **Core/Support/universe.py**
- **Core/Support/config.py**
- **pymongo**
- **quandl**
- **pandas**
- **os**
___

### Files used in:
- **Core/Backtest/SENO.py**
- **Core/Backtest/SENQ.py**
- **Core/Support/evaluate.py**
___

## Classes Used:
- **DataRegistry**
___
#### Class Methods:
- str
___
#### Instance Methods:
- **routineCheckup**
- **updateRegistries**
- **individualData**
- **everythingExists**
- **addDataRegistry**
- **deleteDataRegistry**
- **getdata**
___
#### Class Variables:
- **DetailsPath**
##### datatype: String
##### default:getcwd()+"\\objectDetails\\DataRegistry.txt"
___
#### Instance Variables:

- **startDate**
##### datatype:string
##### default:"2008-05-31"
___
- **endDate**
##### datatype:string
##### default:"2018-05-31"
___
- **eqList**
##### datatype:List
##### default:universe.Universe().listUniverseTickers('nifty500')
___
- **dbName**
##### datatype:string
##### default:"nse_data_registry"
___
- **dataSource**
##### datatype:string
##### default:"quandl"
___
- **connectionInfo**
##### datatype:string
##### default:config.defaultConnectionInfo
___
- **dataRegistries**
##### datatype:list
##### default:list(config.dataRegistries.keys())
___
- **client**
##### datatype: MongoClient object
##### default:None
___
- **db**
##### datatype:pymongo Database reference
##### default:None
___
- **registry**
##### datatype:pymongo Registry reference
##### default:None
___
- **returnedDF**
##### datatype:pandas dataframe
##### default:None
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
def __init__(self,startDate,endDate,eqList,dataSource,databaseName,registryList,connectionInfo,debug,isUser)
```

##### Inputs: string,string,List,string,string,List,string,boolean,boolean
##### Input Defaults: '2008-05-31','2018-05-31',universe.Universe().listUniverseTickers('nifty500'),"quandl",
##### "nse_data_registry",list(config.dataRegistries.keys()),config.defaultConnectionInfo,
##### config.debug,False
##### Outputs: None
##### Access: public
##### Operation Flow:

```python
try:
    self.startDate=startDate
    self.endDate=endDate
    self.eqList=eqList
    self.connectionInfo=connectionInfo
    self.dbName=databaseName
    self.dataSource=dataSource
    self.dataRegistries=config.dataRegistries
     
    self.client=pymongo.MongoClient(self.connectionInfo)
    self.db=self.client[self.dbName]
   
    if debug:
        self._routineCheckup()
except:
    return "InputAcceptanceError" 
```
___
### Instance Methods
___
#### routineCheckup

##### Inputs: None
##### Input Defaults: NA
##### Outputs: String(only in case of error)
##### Access: private
##### Operation: Just a function to perform routine checkup of the registries.Not run normally by user.Only by admin.
___

#### updateRegistries

##### Inputs: None
##### Input Defaults: NA
##### Outputs: string
##### Access: private
##### Operation: Checks if the registry is updated or not
___

#### individualData

##### Inputs: string,string
##### Input Defaults: None
##### Outputs: dataframe/error
##### Access: private
##### Operation: Loads a single attribute of a single equity ticker if the dataSource is set as quandl
___

#### addDataRegistry

##### Inputs:string
##### Input Defaults: None
##### Outputs: None
##### Access: private
##### Operation: Whenever the variable config.dataRegistries changes or the database is corrupted, this method will be executed and the new registries will be added to our current ones.
___

#### getdata

##### Inputs: string,string
##### Input Defaults: None
##### Outputs: None
##### Access: public
##### Operation: Sets the returnedDF parameter of the DataRegistry type object to the requested attribute for the given stocklist.Can also be called as getData or get_data.
___

#### deleteDataRegistry

##### Inputs: databaseReference,names
##### Input Defaults: all
##### Outputs: None
##### Access: private
##### Operation:  In case of any major change in the way data is retrieved or stored this function can be used to empty the existing data registry
___

    

    
    
    
    
