
filename = ""
posix_file = posix()
posix_file.set_size(3999999999999999)
RAID.read_file(posix_file)
RAID.write_file(posix_file)
stat(posix_file)
