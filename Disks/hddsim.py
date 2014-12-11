import random
import math

class HDD:
    #'Common base class for all Hard Disk Drives (HDD)'
   hdd_amount = 0
   
   #HDD ATTRIBUTES
   addressesData = [] # store data here
   log_report = [] #variable to keep track of transactions
   head_position = 0
   capacity = 0
   hdd_block_amount =0
   blockSize = 0
   TotalUseTime = 0
   
   #PREDEFINED HDD ATTRIBUTES
   Transfer_Time = 0.05 #ms 20,000 blocks/second
   Rotational_Latency = 8.333 #ms for entire revolution (7200 RPM = 120 rev/sec = 8.333ms/rev)
   Seek_time = 5 #ms
   time_to_fail = 36000000000 #10000 hours in ms

   def __init__(self, capacity, blockSize):
      self.capacity = capacity
      self.blockSize = blockSize
      self.hdd_block_amount = capacity / blockSize; #calculate amount of blocks
      self.addressesData = [None]*self.hdd_block_amount # create empty list of size hdd_block_amount
      HDD.hdd_amount += 1 #keep track of HDD amount
      self.TotalUseTime = 0
   
   
   def displayCapacity(self):
     print "Total Capacity %d" % self.capacity

   def displaySeek_Time(self):
      print "Total Seek Time %d" % self.Seek_time

   #method to write to a single block in memory & return statistics
   def writeToAddress(self, address_add, data):
      if len(self.addressesData) > address_add:
         self.addressesData[address_add] = data;
         head_position = random.randint(0,len(self.addressesData))
         percentage = math.fabs(head_position - address_add) / len(self.addressesData)
         rotation_time = (percentage * self.Rotational_Latency)
         returnTime = self.Seek_time+rotation_time+self.Transfer_Time
         logAction = 'Write to '+str(address_add)+' in '+str(returnTime)+' mseconds'
         self.log_report.append(logAction)
         self.TotalUseTime += returnTime
         return returnTime
      else:
         return 0

   #Call the method to write a single block x amount of times & return entire statistics
   def write(self,blocks):
      stats = 0
      for b in blocks:
         stats += self.writeToAddress(b,0)
      return stats

   #method to read from a single block in memory & return statistics
   def readFromAddress(self, address_read):
      head_position = random.randint(0,len(self.addressesData))
      percentage = math.fabs(head_position - address_read) / len(self.addressesData)
      rotation_time = (percentage * self.Rotational_Latency)
      if address_read > 0 and address_read < len(self.addressesData):
         time = self.Seek_time+rotation_time+self.Transfer_Time         
         logAction = 'Read from '+str(address_read)+' in '+str(time)+' mseconds'
         self.TotalUseTime += time
         return time
         #return HDD.addressesData[address_read]
      return 0

   def read(self,blocks):
      stats = 0
      for b in blocks:
         stats += self.readFromAddress(b)
      return (stats,-1)

   def checkDisk(self):
      if (self.TotalUseTime < self.time_to_fail):
         # True means the disk is ok
         return True
      else:
         return False



   # Rotational/Hard Drive:  Seek Time + Rotational Latency + Transfer Time
   def data_retrieval_time(self):
      if address_read > 0 and address_read < len(self.addressesData):
         return self.Seek_time+self.Rotational_Latency+self.Transfer_Time

   def getDisk(self):
      return self

   #save log to a file
   def writeLogToFile(self,name):
      file = open(name,'w')
      for item in self.log_report:
        file.write("%s\n" % item)
      file.close()
    

    #method to reset all the variables of the disk
   def reset(self):
        self.addressesData = [] # store data here
        self.log_report = [] #variable to keep track of transactions
        self.head_position = 0
        self.capacity = 0
        self.hdd_block_amount =0
        self.blockSize = 0
        self.TotalUseTime = 0





