#!/usr/bin/env
import sys
sys.path.insert(0, '../Disks')

import ssdsim
import hddsim

import numpy as np
import scipy.stats as sst
import math

class RAID():
	def __init__(self, RAIDtype=0, disknumber=5, flashpercent=0.2, SSDcapacity=250, HDDcapacity=250, blocksize=4096):
		self.Rtype = RAIDtype
		self.NoOfDisks = disknumber
		self.blocksize = blocksize
		self.disks = []
		#self.disks = np.array([self.NoOfDisks], type=ctypes_py_object)
		self.flashpercent = flashpercent
		# Disk type array for each disk. Type 0 = HDD, Type 1 = SDD
		self.disktype = np.zeros([self.NoOfDisks])
		for i in range(int(self.NoOfDisks * self.flashpercent)):
			self.disktype[i] = 1
		# The dictionary that will map inodes to disks and blocks
		self.filemap = {}
		# array with the number of blocks in each disk
		self.diskBlocksNum = np.zeros([self.NoOfDisks])
		# For each disk, we store a boolean array that shows 
		# if every block is available (1) or not (0)
		self.diskBlocks = []
		for i in range(self.NoOfDisks):
			if (self.disktype[i] == 0):
				tempcapacity = HDDcapacity*1000000000
				self.disks.append(hddsim.HDD(tempcapacity, blocksize))
				#self.disks[i] =  hddsim.HDD(tempcapacity, blocksize)
				self.diskBlocksNum[i] = int(tempcapacity) / int(blocksize)
				self.diskBlocks.append(np.ones([self.diskBlocksNum[i]]))
			else:
				tempcapacity = SSDcapacity*1000000000
				self.disks.append(ssdsim.SSD(tempcapacity, blocksize))
				#self.disks[i] = ssdsim.SSD(tempcapacity, blocksize)
				self.diskBlocksNum[i] = int(tempcapacity)/int(blocksize)
				self.diskBlocks.append(np.ones([self.diskBlocksNum[i]]))

		#self.__read(fname, fsize)
		#self.__write(fname, fsize)
		#self.__delete(fname, fsize)

	def read(self, posfile):
		#do stuff in RAID arrays
		print "Will read ", posfile.get_file(), " with size ", posfile.get_size()
	def write(self, posfile):
		#do stuff in RAID arrays
		print "Will write ", posfile.get_file(), " with size ", posfile.get_size()
	def delete(self, posfile):
		#do stuff in RAID arrays
		print "Will delete ", posfile.get_file(), " with size ", posfile.get_size()

	__read = read
	__write = write
	__delete = delete

		

	def getRtype(self):
		ans = self.Rtype
		return ans
	def setRtype(self, Rtype):
		if (checkRType(Rtype)):
			self.Rtype = Rtype
	def checkRType(self, R):
		if ((R == 0) or (R==1) or (R==5)):
			return True
		else:
			return False



class RAID0(RAID):
	def write(self, posfile):
		size = posfile.get_size()
		name = posfile.get_file()
		NoOfBlocks = int(size) / int(self.blocksize)

		#Compute the stripe size
		StripeSize = int(NoOfBlocks) / int(self.NoOfDisks)
		# One extra block might be needed to some stripes
		Extra = NoOfBlocks % self.NoOfDisks
		d = 0
		adresses = {}
		# Check if we have enough space in the RAID array
		if (self.checkForSpace(StripeSize+1)):
			d = 0
			xx = Extra
			while (d < self.NoOfDisks):
				#get a list of the available blocks in the disk d
				availblocks = np.nonzero(self.diskBlocks[d])[0]
				if (len(availblocks) >= StripeSize + 1):
					if (xx > 0):
						writeblocks = availblocks[0:StripeSize + 1]
						xx -= 1
					else:
						writeblocks = availblocks[0:StripeSize]
				else:
					writeblocks = availblocks[0:StripeSize]

				# Write in these blocks
				currentDisk = self.disks[d].getDisk()
				answer = currentDisk.write(writeblocks)
				#print "\t\tRAID Disk: ", d, ", write to blocks ", writeblocks
				#print "\t\t\tTime needed: ", answer, " ms"

				#Write was succesfull
				#Calculate statistics from answer

				# These blocks become unavailable
				adresses[d] = writeblocks
				self.diskBlocks[d][writeblocks] = 0
				# Move on to the next disk
				d += 1
			# We completed the write to all disks.
			# Update the map of the files for future acceses
			self.filemap[name] = adresses
			return 1
		else:
			# Not enough space in the disks
			#print "Not enough space!!"
			return -2

	def read(self, posfile):
		name = posfile.get_file()
		if (name in self.filemap):
			# We have written this file before and it exists in our filemap of the RAID array
			adresses = self.filemap[name]
			for d, blocks in adresses.iteritems():
				currentDisk = self.disks[d].getDisk()
				answer = currentDisk.read(blocks)
				#Calculate statistics from answer
				#print "\t\tRAID disk ", d, ", read blocks ", blocks
				#print "\t\t\tTime needed: ", answer[0], " ms"

			# We read all blocks from all disks
			return 1
		else:
			#print "Error! File does not exist!"
			return -1

	def delete(self, posfile):
		name = posfile.get_file()
		if (name in self.filemap):
			# We have written this file before and it exists in our filemap of the RAID array
			adresses = self.filemap[name]
			for d, blocks in adresses.iteritems():
				# Just make these blocks available again - not really delete them
				self.diskBlocks[d][blocks] = 1
				#print "\t\tRAID disk ", d, ", blocks ", blocks, " are available again."
			# We made all blocks from all disks available
			return 1
		else:
			#print "Error! File does not exist!"
			return -1

	def checkForSpace(self, stripesize):
		d = 0
		ans = False
		while (d < self.NoOfDisks):
			if (np.sum(self.diskBlocks[d]) >= stripesize):
				d += 1
			else:
				break
		if  (d < self.NoOfDisks):
			return False
		else:
			return True


	'''def checkForSpace(self, stripesize, extra):
		d = 0
		x = extra
		ans = False
		while ((x > 0) and (d < self.NoOfDisks)):
			if (np.sum(self.diskBlocks[d]) >= stripesize + 1):
				x -= 1
				d += 1
			elif (np.sum(self.diskBlocks[d]) >= stripesize):
				d += 1
			else:
				break
		if  ((d < self.NoOfDisks) or (x > 0)):
			return False
		else:
			return True
	'''


class RAID5(RAID):
	def write(self, posfile):
		size = posfile.get_size()
		name = posfile.get_file()
		NoOfBlocks = int(size) / int(self.blocksize)

		#Compute the stripe size
		StripeSize = int(NoOfBlocks) / int(self.NoOfDisks)
		# One extra block might be needed to some stripes
		Extra = NoOfBlocks % self.NoOfDisks
		if (Extra > 0):
			StripeSize += 1
		d = 0
		adresses = {}

		RetArr = np.zeros([10])
		

		# Check if we have enough space in the RAID array
		if (self.checkForSpace(StripeSize+1)):
			d = 0
			while (d < self.NoOfDisks):
				#get a list of the available blocks in the disk d
				availblocks = np.nonzero(self.diskBlocks[d])[0]
				# We will need to write to Stipesize + 1 (for parity) blocks
				writeblocks = availblocks[0:StripeSize + 1]

				# Write in these blocks
				currentDisk = self.disks[d].getDisk()
				#print "\t\tRAID Disk: ", d, ", write to blocks ", writeblocks
				answer = currentDisk.write(writeblocks)
				#print "\t\t\tTime needed: ", answer, " ms"
				
				RetArr[d] = answer

				#Calculate statistics from answer

				#Write was succesfull
				adresses[d] = writeblocks
				#Make these blocks unavailable
				self.diskBlocks[d][writeblocks] = 0
				# Move on to the next disk
				d += 1
				# If we wrote the extra blocks needed
				if (d==Extra):
					StripeSize -= 1
			# We completed the write to all disks.
			# Update the map of the files for future acceses
			self.filemap[name] = adresses
			return RetArr
		else:
			# Not enough space in the disks
			#print "Not enough space!!"
			return -2

	def read(self, posfile):
		name = posfile.get_file()
		if (name in self.filemap):
			# We have written this file before and it exists in our filemap of the RAID array
			RetArr = np.zeros([10])
			adresses = self.filemap[name]
			for d, blocks in adresses.iteritems():
				currentDisk = self.disks[d].getDisk()
				answer = currentDisk.read(blocks)
				#print "\t\tRAID disk ", d, ", read blocks ", blocks
				#print "\t\t\tTime needed: ", answer[0], " ms"

				RetArr[d] = answer[0]
				#print "Read blocks ", blocks, " from disk ", d, ". Time needed: ", answer[0]
				# Calculate statistics from answer


			# We read all blocks from all disks
			return RetArr
		else:
			#print "Error! File does not exist!"
			return -1

	def delete(self, posfile):
		name = posfile.get_file()
		if (name in self.filemap):
			# We have written this file before and it exists in our filemap of the RAID array
			adresses = self.filemap[name]
			for d, blocks in adresses.iteritems():
				# Just make these blocks available again - not really delete them
				self.diskBlocks[d][blocks] = 1
				#print "\t\tRAID disk ", d, ", blocks ", blocks, " are available again."
			# We made all blocks from all disks available
			return 1
		else:
			#print "Error! File does not exist!"
			return -1

	def checkDisks(self, filename, itert):
		for d in range(self.NoOfDisks):
			if (not (self.disks[d].getDisk()).checkDisk()):
				with open(filename, "a") as myfile:
					myfile.write(str[d] + "\t" + str(itert))



	def checkForSpace(self, stripesize):
		d = 0
		ans = False
		while (d < self.NoOfDisks):
			if (np.sum(self.diskBlocks[d]) >= stripesize):
				d += 1
			else:
				break
		if  (d < self.NoOfDisks):
			return False
		else:
			return True







