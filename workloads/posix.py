

class Posix:
    #"""The Stard POSIX inode Attributes"""
    def __init__(self):
        self.file = name               # String with the name of the file (and filepath)
        size = -1               # Positive integer with the size of the file
        blocks = 0              # Number of blocks this file takes up on disk 
                                     # (may actually take up more based on replication, but not seen here)
        ioblock = 4096          # Dunno if this will ever change
        file_type = "regular"   # No idea what other types are
        device = "14h/20d"      # RAID Device, but don't see more specific here
        inode = 0               # The inode on the file system
        links = 1               # Number of HARD links to this inode
        access = 0000           # No permisions. Always 0 start Chmod +x 777 -> 0777
        uid = 0                 # User ID of file's owner
        gid = 0                 # Group ID of the file
        m_access = 1414178401   # Unix Timestamp (2014-10-24T19:20:01Z)
        m_modify = 1414178401   # Unix Timestamp (2014-10-24T19:20:01Z)
        m_change = 1414178401   # Unix Timestamp (2014-10-24T19:20:01Z)

    def set_file(self, name):
        self.file = name

    def get_file(self):
        return self.file

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks

    def set_ioblock(self, ioblock):
        self.ioblock = ioblock

    def get_ioblock(self):
        return self.ioblock

    def set_file_type(self, file_type):
        self.file_type = file_type

    def get_file_type(self):
        return self.file_type

    def set_device(self, device):
        self.device = device

    def get_device(self):
        return self.device

    def set_inode(self, inode):
        self.indoe = inode

    def get_inode(self):
        return self.inode

    def set_links(self, links):
        self.links = links

    def get_links(self):
        return self.links

    def set_access(self, access):
        self.access = access

    def get_access(self):
        return self.access

    def set_uid(self, uid):
        self.uid = uid

    def get_uid(self):
        return self.uid

    def set_gid(self, gid):
        self.gid = gid

    def get_gid(self):
        return self.gid

    def set_m_access(self, m_access):
        self.m_access = m_access

    def get_m_access(self):
        return self.m_access

    def set_m_modify(self, m_modify):
        self.m_modify = m_modify

    def get_m_modify(self):
        return self.m_modify

    def set_m_change(self, m_change):
        self.m_change = m_change

    def get_m_change(self):
        return self.m_change

    def stat(self):
        print self.get_file
        print self.get_size,
        print self.get_blocks,
        print self.get_ioblock,
        print self.get_file_type
        print self.get_device,
        print self.get_inode,
        print self.get_links
        print self.get_access,
        print self.get_uid,
        print self.get_gid
        print self.get_m_access
        print self.get_m_modify
        print self.get_m_change
