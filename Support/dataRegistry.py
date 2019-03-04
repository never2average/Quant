# -*- coding: utf-8 -*-

import os
import universe
import config
import pandas as pd

import quandl
from quandl.errors.quandl_error import NotFoundError
quandl.ApiConfig.api_key=config.quandlKey

import pymongo


class DataRegistry:

    DetailsPath=os.getcwd()+"\\objectDetails\\DataRegistry.txt"
    def __str__(self):
        #Obtain object details on the fly in command line
        fobj=open(DataRegistry.DetailsPath,"r")
        details=fobj.read()
        fobj.close()
        return details

    def __init__(self
                 ,startDate='2008-05-31'
                 ,endDate='2018-05-31'
                 ,eqList=universe.Universe().listUniverseTickers('nifty500')
                 ,dataSource="quandl"
                 ,databaseName="nse_data_registry"
                 ,registryList=list(config.dataRegistries.keys())
                 ,connectionInfo=config.defaultConnectionInfo
                 ,debug=config.debug
                 ,isUser=False):

        try:
            #Initialize Parameters
            self.startDate=startDate
            self.endDate=endDate
            self.eqList=eqList
            self.connectionInfo=connectionInfo
            self.dbName=databaseName
            self.dataSource=dataSource
            self.dataRegistries=config.dataRegistries

            #Connect to the database
            self.client=pymongo.MongoClient(self.connectionInfo)
            self.db=self.client[self.dbName]

            #Performs routinecheckup when run in debug mode
            if debug:
                self._routineCheckup()
        except:
            return "InputAcceptanceError"

    def _routineCheckup(self):
        """
        Just a function to perform routine checkup of the registries.Not run
        normally by user.Only by admin.
        """
        try:
            self.existingRegistries=self.db.list_collection_names()
            if self.existingRegistries!=self.dataRegistries:
                self._updateRegistries()
        except:
            return "RoutineCheckupError"

    def _updateRegistries(self):
        """
        Checks if the registry is updated or not
        """
        try:
            for registry in self.existingRegistries:
                if registry not in self.dataRegistries:
                    self.db.drop_collection(registry)
            for registry in self.dataRegistries:
                if registry not in self.existingRegistries:
                    self._addDataRegistry(registry)
            return "RegistryDataUpdateSuccessfull"
        except:
            return "RegistryUpdateError"

    def _individualData(self,name,columnName):
        """
        Function to fetch one data attribute for any one stock
        """
        if self.dataSource=="quandl":
            try:
                return quandl.get('NSE/{}.{}'.format(name.replace('&','').replace('-','_'),config.dataRegistries[columnName])
                                  ,start_date=self.startDate
                                  ,end_date=self.endDate)
            except NotFoundError:
                return "DataRegistryCompilationError"

    def _addDataRegistry(self,columnName):
        """
        Whenever the variable config.dataRegistries changes or the database
        is corrupted, this method will be executed and the new registries will
        be added to our current ones.
        """
        individualDfs=[]
        for ticker in self.eqList:
            print(ticker)
            singleStockData=self._individualData(ticker,columnName)
            individualDfs.append(singleStockData)
        df=pd.concat(individualDfs,axis=1,sort=True)
        del individualDfs
        df.columns=self.eqList
        df.reset_index(level=0,inplace=True)

        self.registry=self.db[columnName]

        self.registry.insert_many(df.to_dict('records'))
        print("{} has been added to database".format(columnName))


    """
    Call any of the below three methods to get a dataframe of any particular
    attribute(given it exists) and then filter it for your choice of stocks
    """
    def getdata(self,
                registryname,
                stockList):

        self.returnedDF=pd.DataFrame(list(self.db[registryname].find({}, {"_id":0})))
        self.returnedDF.set_index(["Date"],inplace=True)
        self.returnedDF=self.returnedDF[stockList]

        self.returnedDF=self.returnedDF.fillna(method=
                'ffill').fillna(method='bfill')

    def getData(self,registryname,stockList):
        self.getdata(registryname,stockList)

    def get_data(self,registryname,stockList):
        self.getdata(registryname,stockList)


    def _deleteDataRegistry(self,db,names="all"):

        """
        In case of any major change in the way data is retrieved or stored
        this function can be used to empty the existing data registry
        """

        if names=="all":
            self.client.drop_database(db)
        else:
            for i in names:
                self.client[db].drop_collection(i)
DataRegistry(isUser=True)