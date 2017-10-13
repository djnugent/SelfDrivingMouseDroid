import os
from time import sleep

def trainOn(modelData, resultNumbers=[]):
      for dataset in modelData["datasets"]:
            print("dataset: " + str(dataset))
      num = 100 
      resultNumbers.append(num)
      while (num > 1): 
            num = num / 1.5
            print("epoch - globalNum is " + str(num))
            resultNumbers.append(num)       
            sleep(10)
      print ('training thread all done')
      #store resultNumbers in a file somewhere, along with ModelName, notes, etc.
      del resultNumbers[:]
      return 
