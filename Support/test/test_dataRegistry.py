# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import unittest
import universe
import config
from dataRegistry import DataRegistry
 
class TestDataRegistry(unittest.TestCase):
 
    def setUp(self):
        self.TestObject=universe.Universe(databaseName="universes",
                 universeList=list(config.universes.keys()),
                 connectionInfo='mongodb://localhost:27017/',
                 routineCheckup=True,
                 isUser=False)
        self.TestRegistry=DataRegistry()
        #Verify that no error has been made in providing input
        self.assertNotEqual(self.TestObject,"InputAcceptanceError")
 
    def routineCheckupTest(self):
        #Verify Whether or not there is an error in routinecheckup
        self.assertNotEqual(self.TestObject.routineCheckup(),"RoutineCheckupError")
        
    def updateUniversesTest(self):
        #Verify Whether or not there is an error encountered while updating databases
        self.assertNotEqual(self.TestObject.routineCheckup(),"UniverseUpdateError")
        self.assertEqual(self.TestObject.existingUniverses,self.TestObject.universes)
    
if __name__ == '__main__':
    unittest.main()