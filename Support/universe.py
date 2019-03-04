# -*- coding: utf-8 -*-

import config
import csv
from requests import Session
import pymongo
import os

class Universe:


    DetailsPath=os.getcwd()+"\\objectDetails\\Universe.txt"

    def __str__(self):
        fobj=open(Universe.DetailsPath,"r")
        details=fobj.read()
        fobj.close()
        return details

    def __init__(self,
                 databaseName="universes",
                 universeList=list(config.universes.keys()),
                 connectionInfo=config.defaultConnectionInfo,
                 routineCheckup=True,
                 isUser=True):
        try:
            self.universes=universeList
            self.dbName=databaseName
            self.isUser=isUser
            self.connectionInfo=connectionInfo
            if routineCheckup:
                self.routineCheckup()
        except:
            return "InputAcceptanceError"

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

    def _updateUniverses(self):
        try:
            for universe in self.existingUniverses:
                if universe not in self.universes:
                    self.db.drop_collection(universe)
            for universe in self.universes:
                if universe not in self.existingUniverses:
                    self._addUniverse(universe)
            return "UniversesDataUpdateSuccessfull"
        except:
            return "UniverseUpdateError"

    def _addUniverse(self,universe):
        universeCollection=self.db[universe]
        startUrl=config.urlBase[config.universes[universe]].format(universe)
        with Session() as additionSession:
            csvContent=additionSession.get(startUrl).content.decode('utf-8')
            cleanedCSV=list(csv.reader(csvContent.splitlines(), delimiter=','))
            cleanedCSV=self._convertPosts(cleanedCSV)
            universeCollection.insert_many(cleanedCSV[1:])

    def _convertPosts(self,postsList):
        n=len(postsList)
        for post in range(n):
            postsList[post]={"ticker":postsList[post][2],"industry":postsList[post][1]}
        return postsList

    def listUniverseTickers(self,universe):
        try:
            return [i["ticker"] for i in self.db[universe].find({},{"ticker":1,"_id":0})]
        except:
            return "StockTickerReturnError"
    def listUniverseTickersByIndustry(self,universe):
        try:
            return [i for i in self.db[universe].find({},{"_id":0})]
        except:
            return "StockTickerReturnError"
