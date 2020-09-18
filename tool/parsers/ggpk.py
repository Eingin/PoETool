import struct

class Entry:
    def __init__(self, reader):
    self.recordLength, self.tag = struct.unpack("II", reader.read(8))

class GGPKEntry:
    def __init__(self, entry: Entry, reader):
        def __init__(self, reader)
        self.version, = struct.unpack("I", reader.read(4))
        self.offsets = struct.unpack("II", reader.read(8))


class FileEntry:
        def __init__(self, entry: Entry, reader)
        self.nameLength, = struct.unpack("I", reader.read(4))
        self.signature, = struct.unpack("32B", reader.read(32*8))
        self.name = reader.read(self.nameLength).decode('utf-16')
        self.dataOffset = reader.tell()

class ChildEntry:
    def __init__(self, reader)
        self.hash, self.offset, = struct.unpack("IQ", reader.read(12))

class PDirEntry:
        def __init__(self, entry: Entry, reader)
        self.nameLength, self.childCount, = struct.unpack("II", reader.read(8))
        self.signature, = struct.unpack("32B", reader.read(32*8))
        self.name = reader.read(self.nameLength).decode('utf-16')
        self.children = []
        for _ in range(self.childCount):
            self.children.append(ChildEntry(reader))

class FreeEntry:
        def __init__(self, entry: Entry, reader)
        self.next, = struct.unpack("q", reader.read(8))

class GGPK:
     def __init__(self, reader):