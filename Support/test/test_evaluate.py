# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from evaluate import CustomInputEvaluator

def customTest():
    testObject=CustomInputEvaluator(rawString="Close-Open"
                                         ,stockList=["ITC","TITAN"]
                                         ,debug=True,
                                         normalizeInput=True)
    print(testObject.normalizedResult.head(1))
        
if __name__=="__main__":
    customTest()
