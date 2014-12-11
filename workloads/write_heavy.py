#!/usr/bin/env
import sys
sys.path.insert(0, '../RAID')
sys.path.insert(0, '../workloads')
sys.path.insert(0, '../Disks')
import math
import matplotlib.pyplot as plt
import RAIDinterface
import ssdsim
import hddsim
import posixsim as psx
import numpy as np
import random
#from posix import Posix as psx


def simulate():

	# New RAID interface
	R0 = RAIDinterface.RAID0(RAIDtype=0, disknumber=10, flashpercent=0.2, SSDcapacity=250, HDDcapacity=250, blocksize=4096)
	R5 = RAIDinterface.RAID0(RAIDtype=0, disknumber=10, flashpercent=0.2, SSDcapacity=250, HDDcapacity=500, blocksize=4096)

	# Distribution of possible operations
	action_set = ["write","read","write","write","read","write","write","write","delete"]

	#Loop
	
	# Number of iterations to run
	N = 1000000000
	#Empty list to store filenames so as to read from existing files
	files = []
	for ii in xrange(1,N):
		#create workload
		# tw random number in [0,9]. To choose workload based on balance.
		# Set boundary to 5 if balaned, or to 3 or 7 for unbalanced workload

		#tw = random.randint(0,9)
		current_action = random.choice(action_set)
		if current_action == "write":
		#if (tw < Bound):
			#work = 'w'
			# A good random name is the number of the iteration: ii
			f = psx.Posix(str(ii))
			files.append(f)
			randomSize = random.randint(100,1000000000)
			f.set_size(randomSize)
			ans = R5.read(f)
			print iter, 'w', f.get_size(), np.array_str(ans)
		elif current_action == "read":
			#work = 'r'
			#Choose random file from list
			#randfileind = random.randint(0,len(files)-1)
			#f = files[randfileind]
			f = random.choice(files)
			ans = R5.write(f)
			print iter, 'r', f.get_size(), np.array_str(ans)
		elif current_action == "delete":
			f = random.choice(files)
			R5.delete(f)
		else:
			print "I shouldn't be here"


		# After each execution, check if any disk needs to change
		for i in range(disknumber):
			R5.checkDisks("ChangeDisksLog.csv", ii)
