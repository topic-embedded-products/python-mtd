# SPDX-License-Identifier: MIT
# Methods to interact with MTD, Memory Technology Device
import struct
import mtd
import sys

def flash_compare(mtdstream, filestream, blocksize=65536):
	"""Read filestream and compare contents to mtdstream. Returns
	whether contents match."""
	while 1:
		f = filestream.read(blocksize)
		if not f:
			return True
		m = mtdstream.read(len(f))
		if m != f:
			return False

def flash_is_erased(device, size, sector_size = None):
	"Check if data is all 1s, in that case erase is not needed for NOR"
	if sector_size is None:
		fd = device.fileno()
		t, total_size, sector_size = mtd.get_info(fd)
		if size > total_size:
			raise Exception, "File is too large: %d > %d" % (size, total_size)
	ones = '\xff' * sector_size
	start = 0;
	while start < size:
		d = device.read(sector_size)
		if d != ones:
			return False
		start += sector_size
	return True

def flash_erase(device, size, sector_size = None, verbose = True):
	"Erase enough to fit size bytes"
	fd = device.fileno()
	if sector_size is None:
		t, total_size, sector_size = mtd.get_info(fd)
		if size > total_size:
			raise Exception, "File is too large: %d > %d" % (size, total_size)
	start = 0;
	while start < size:
		if verbose:
			sys.stderr.write("erase %d/%d\r" % (start, size))
		mtd.erase_sector(fd, start, sector_size)
		start += sector_size

def flash_update(mtddev, filename, verbose = True):
	"""Write file to MTD device, only rewriting if contents do not match."""
	# Open the file
	with open(filename, 'rb', 0) as fd:
		fd.seek(0, 2) # EOF
		file_size = fd.tell()
		fd.seek(0)
		# open the mtd
		with open(mtddev, 'r+', 0) as device:
			t, total_size, sector_size = mtd.get_info(device.fileno())
			if total_size < file_size:
				raise Exception, "%s (%d) won't fit in %s (%d)" % (filename, file_size, mtddev, total_size)
			if flash_compare(device, fd, sector_size):
				if verbose:
					sys.stderr.write("Skip %s: %s, contents are equal\n" % (mtddev, filename))
				return 0
			# Erase enough flash to fit
			device.seek(0)
			if not flash_is_erased(device, file_size, sector_size):
				flash_erase(device, file_size, sector_size, verbose)
			device.seek(0)
			fd.seek(0)
			# Write data
			start = 0
			while 1:
				d = fd.read(sector_size)
				if not d:
					break
				start += len(d)
				if verbose:
					sys.stderr.write("write %d/%d\r" % (start, file_size))
				device.write(d)
			# Verify
			fd.seek(0)
			device.seek(0)
			if not flash_compare(device, fd, sector_size):
				raise Exception, "Flash verification failed"
			if verbose:
				sys.stderr.write("%s: %s, %d/%d bytes\n" % (mtddev, filename, file_size, total_size))
	return file_size
