import os
from time import sleep

def trainOn(trainingDatasets=[], resultNumbers=[]):
      for dataset in trainingDatasets:
            print("here " + str(dataset))
      num = 100 
      resultNumbers.append(num)
      while (num > 0): 
            num = num / 1.5
            print("epoch - globalNum is " + str(num))
            resultNumbers.append(num)       
            sleep(10)
      print ('training thread all done')
      return 
