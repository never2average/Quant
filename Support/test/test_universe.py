# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from universe import Universe
import config
import unittest
 
class TestUniverse(unittest.TestCase):
 
    def setUp(self):
        self.testObject=Universe(databaseName="universes",
                 universeList=list(config.universes.keys()),
                 connectionInfo='mongodb://localhost:27017/',
                 routineCheckup=False)
        #Verify that no error has been made in providing input
        self.assertNotEqual(self.testObject,"InputAcceptanceError")
 
    def routineCheckupTest(self):
        #Verify Whether or not there is an error in routinecheckup
        self.assertNotEqual(self.testObject.routineCheckup(),"RoutineCheckupError")
        
    def updateUniversesTest(self):
        #Verify Whether or not there is an error encountered while updating databases
        self.assertNotEqual(self.testObject.routineCheckup(),"UniverseUpdateError")
        self.assertEqual(self.testObject.existingUniverses,self.testObject.universes)
    
if __name__ == '__main__':
    unittest.main()
