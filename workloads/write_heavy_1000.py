#!/usr/bin/env
import sys
sys.path.insert(0, '../RAID')
sys.path.insert(0, '../workloads')
sys.path.insert(0, '../Disks')
import math
import matplotlib.pyplot as plt
import random
import RAIDinterface
import ssdsim
import hddsim
import posixsim as psx
import numpy as np

# New posix files
pf_1 = psx.Posix('a.dat')
pf_2 = psx.Posix('b.dat')
pf_3 = psx.Posix('c.dat')
pf_4 = psx.Posix('d.dat')

# Set its size
pf_1.set_size(1000000)
pf_2.set_size(100000)
pf_3.set_size(5000)
pf_4.set_size(3000000)

# Different Possible Files
pf_set = [pf_1,pf_2,pf_3,pf_4]

# Distribution of possible operations
action_set = ["write","read","write","write","read","write","write","write"]


# Set up RAID
current_RAID = RAIDinterface.RAID0(RAIDtype=0, disknumber=10, flashpercent=0.2, SSDcapacity=250, HDDcapacity=500, blocksize=4096)

# Outputs
output_list = []

for i in xrange(0,1000):

  current_pf = random.choice(pf_set)
  current_action = random.choice(action_set)

  #print current_pf.get_file()

  if current_action == "write":
    current_output = current_RAID.write(current_pf)
  if current_action == "read":
    current_output = current_RAID.read(current_pf)
  if current_action == "delete":
    current_output = current_RAID.delete(current_pf) #TODO: Does this break things?
  else:
    print "I shouldn't be here"

  output_list.append(current_output)


