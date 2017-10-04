import os
from time import sleep

def trainOn(trainingDatasets=[], resultNumbers=[]):
      for dataset in trainingDatasets:
            print("here " + str(dataset))
      num = 0 
      while (num < 6): 
            sleep(10)
            num += 2
            print("epoch - globalNum is " + str(num))
            resultNumbers.append(num)       

      print ('training thread all done')
      return 
