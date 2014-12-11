import numpy as np

class SSD:
  'Common base class for all Solid State Drives (SSD)'
  ssd_amount = 0
  ssd_page_amount =0;
  writeLimit = []
  addressesData = []
  capacity = 0
  badBlocks = [] #contains the index of the corrupted blocks/pages


  log_report = [] #variable to keep track of transactions

  #Predefined SSD ATTRIBUTES
  Transfer_Time = 0.05 #ms
  Seek_time = 5 #ms
  write_time = 0.002127659574 #time in microseconds to write one byte #Write: Up to 470 Bytes/microsecod or 470 mb/s

  def __init__(self, capacity, pageSize): #instead of blocks we have pages on SSD
    self.capacity = capacity
    self.writeLimit = []
    #self.writeLimit = [int]*self.ssd_page_amount

    #self.writeLimit = np.zeros([self.ssd_page_amount], dtype=int) + 100000
    #self.writeLimit = [100000]*self.ssd_page_amount #amount of writes each cell can handle
    self.ssd_page_amount = capacity / pageSize;
    for i in range(self.ssd_page_amount):
      self.writeLimit.append(100000)
    SSD.ssd_amount += 1
    self.addressesData = [None]*self.ssd_page_amount

  def displayCapacity(self):
   print "Total Capacity %d" % self.capacity

  def displayBlocks(self):
    print "Total Blocks %d" % self.ssd_page_amount

  def writeToAddress(self, address_add, data):
    if len(self.addressesData) > address_add:
       
       self.writeLimit[address_add] -= 1
       #if the address is not valid anymore then we add it to the list of unreliable disks
       if self.writeLimit[address_add] < 1:
          self.badBlocks.append(address_add)
       else:
          self.writeLimit[address_add] = self.writeLimit[address_add]-1
       self.addressesData[address_add] = data;
       returnTime = self.Seek_time+self.Transfer_Time + self.write_time
       logAction = 'Write to '+str(address_add)+' in '+str(returnTime)+' mseconds and write limit is: '+str(self.writeLimit[address_add])
       self.log_report.append(logAction)
       return returnTime

  #Call the method to write a single block x amount of times & return entire statistics
  def write(self,blocks):
    stats = 0
    #A BUFFER is used to flush all the writes needed.
    for b in blocks:
      stats += self.writeToAddress(b,0)
    # Also return which blocks/pages have reached their limit so as not to write there
    return stats

  #Solid-State Drive: Seek Time + Transfer Time
  def data_retrieval_time(self):
    return self.seek_time + self.transfer_time

  #'Method to return statistics for reading'
  def readFromAddress(self, blockNumber):
    if ((len(self.addressesData) > blockNumber) and (blockNumber >= 0)):
       returnTime = self.Seek_time+self.Transfer_Time
       logAction = 'Read from '+str(blockNumber)+' in '+str(returnTime)+' mseconds'
       self.log_report.append(logAction)
       #Calculate the amount of blocks that are possibly corrupted
       bB = self.badBlocks
       return (returnTime, bB)
    return (0,0)

  def read(self,blocks):
    stats = 0
    badblocks = self.badBlocks
    for b in blocks:
      ans = self.readFromAddress(b)
      stats += ans[0]
      #badblocks = ans[1]

    return (stats,badblocks)

  def getDisk(self):
    return self

  def CheckDisk(self):
    #If Percentage of blocks that are bad exceeds let's say 50% return False
    if ((len(self.badBlocks)*100)/len(self.addressesData)) > 50:
      return false
    return true

  #save log to a file
  def writeLogToFile(self,name):
    file = open(name,'w')
    for item in self.log_report:
      file.write("%s\n" % item)
    file.close()


  #method to reset all the variables of the disk       
  def reset(self):
      self.ssd_amount = 0
      self.ssd_page_amount =0;
      self.writeLimit = []
      self.addressesData = []
      self.capacity = 0
      self.badBlocks = [] #contains the index of the corrupted blocks/pages


