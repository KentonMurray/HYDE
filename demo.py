#!/usr/bin/env
import sys
sys.path.insert(0, './RAID')
sys.path.insert(0, './workloads')
sys.path.insert(0, './Disks')
import math
import matplotlib.pyplot as plt
import RAIDinterface
import ssdsim
import hddsim
import posixsim as psx
import numpy as np
#from posix import Posix as psx


def simulate():

	# New RAID interface
	#R0 = RAIDinterface.RAID0(RAIDtype=0, disknumber=10, flashpercent=0.2, SSDcapacity=250, HDDcapacity=250, blocksize=4096)
	R5 = RAIDinterface.RAID0(RAIDtype=0, disknumber=10, flashpercent=0.2, SSDcapacity=250, HDDcapacity=500, blocksize=4096)


	resultsFile = "Results.csv"

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

	
	
	#RAID 5 write the files
	print "Operation: Write file ", pf_1.get_file()
	print "---------------------------------------"
	print "\tSize of file in kB is:", pf_1.get_size()/1000.0
	print "\tNumber of blocks required: ", math.ceil(pf_1.get_size()/4096)
	print "\tPassed request to RAID controller"
	f1w = R5.write(pf_1)
	print "---------------------------------------"
	print "Operation: Write file ", pf_2.get_file()
	print "---------------------------------------"
	print "\tSize of file in kB is:", pf_2.get_size()/1000.0
	print "\tNumber of blocks required: ", math.ceil(pf_2.get_size()/4096)
	print "\tPassed request to RAID controller"
	f2w = R5.write(pf_2)
	print "---------------------------------------"
	print "Operation: Write file ", pf_3.get_file()
	print "---------------------------------------"
	print "\tSize of file in kB is:", pf_3.get_size()/1000.0
	print "\tNumber of blocks required: ", math.ceil(pf_3.get_size()/4096)
	print "\tPassed request to RAID controller"
	f3w = R5.write(pf_3)
	print "---------------------------------------"
	print "Operation: Read file ", pf_2.get_file()
	print "---------------------------------------"
	print "\tPassed request to RAID controller"
	f2r = R5.read(pf_2)
	print "---------------------------------------"
	print "Operation: Read file ", pf_1.get_file()
	print "---------------------------------------"
	print "\tPassed request to RAID controller"
	f1r = R5.read(pf_1)
	print "---------------------------------------"
	print "Operation: Read file ", pf_3.get_file()
	print "---------------------------------------"
	print "\tPassed request to RAID controller"
	f3r = R5.read(pf_3)
	print "---------------------------------------"
	
	print "Operation: Delete file ", pf_2.get_file()
	print "---------------------------------------"
	print "\tPassed request to RAID controller"
	R5.delete(pf_2)
	print "---------------------------------------"
	print "Operation: Write file ", pf_4.get_file()
	print "---------------------------------------"
	print "\tSize of file in kB is:", pf_4.get_size()/1000.0
	print "\tNumber of blocks required: ", math.ceil(pf_4.get_size()/4096)
	print "\tPassed request to RAID controller"
	f4w = R5.write(pf_4)
	print "---------------------------------------"
	print "Operation: Read file ", pf_4.get_file()
	print "---------------------------------------"
	print "\tPassed request to RAID controller"
	f4r = R5.read(pf_4)
	print "---------------------------------------"

	
	n = 4
	labels = ('5kB', '100kB', '1MB', '3MB')
	means_HDD = (np.average(f3w[2:]), np.average(f2w[2:]), np.average(f1w[2:]), np.average(f4w[2:]))
	means_SSD = (np.average(f3w[:2]), np.average(f2w[:2]), np.average(f1w[:2]), np.average(f4w[:2]))
	
	fig, ax = plt.subplots()

	index = np.arange(4)
	bar_width = 0.35

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects1 = plt.bar(index, means_HDD, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='HDD')
	rects2 = plt.bar(index + bar_width, means_SSD, bar_width,
                 alpha=opacity,
                 color='r',
                 error_kw=error_config,
                 label='SSD')

	plt.xlabel('File Size')
	plt.ylabel('Average Write Time (ms)')
	plt.title('Average Time for Write')
	plt.xticks(index + bar_width, labels)
	plt.legend()

	plt.show()

	fig.savefig("WriteTime.png", format="png")
	

	n = 4
	labels = ('5kB', '100kB', '1MB', '3MB')
	means_HDD = (np.average(f3r[2:]), np.average(f2r[2:]), np.average(f1r[2:]), np.average(f4r[2:]))
	means_SSD = (np.average(f3r[:2]), np.average(f2r[:2]), np.average(f1r[:2]), np.average(f4r[:2]))
	
	fig, ax = plt.subplots()

	index = np.arange(4)
	bar_width = 0.35

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects1 = plt.bar(index, means_HDD, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='HDD')
	rects2 = plt.bar(index + bar_width, means_SSD, bar_width,
                 alpha=opacity,
                 color='r',
                 error_kw=error_config,
                 label='SSD')

	plt.xlabel('File Size')
	plt.ylabel('Average Read Time (ms)')
	plt.title('Average Time for Read')
	plt.xticks(index + bar_width, labels)
	plt.legend()

	plt.show()

	fig.savefig("ReadTime.png", format="png")
	
	
	

if __name__ == "__main__":
    simulate()

