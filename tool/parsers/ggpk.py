from anytree import Node, RenderTree
from termcolor import cprint, colored
import struct

class Entry:
    def __init__(self, reader):
        self.recordLength, = struct.unpack("I", reader.read(4))
        self.tag = reader.read(4).decode('utf-8')
        
class GGPKEntry:
    def __init__(self, entry: Entry, reader):
        self.entry = entry
        self.version, = struct.unpack("I", reader.read(4))
        self.offsets = struct.unpack("QQ", reader.read(16))


class FileEntry:
        def __init__(self, entry: Entry, reader):
            self.entry = entry
            self.nameLength, = struct.unpack("I", reader.read(4))
            self.signature = struct.unpack("32B", reader.read(32))
            self.name = reader.read(self.nameLength * 2).decode('utf-16').rstrip('\x00')
            self.dataOffset = reader.tell()

class ChildEntry:
    def __init__(self, reader):
        self.hash, = struct.unpack("I", reader.read(4))
        self.offset, = struct.unpack("Q", reader.read(8))

class PDirEntry:
        def __init__(self, entry: Entry, reader):
            self.nameLength, self.childCount, = struct.unpack("II", reader.read(8))
            self.signature = struct.unpack("32B", reader.read(32))
            self.name = reader.read(self.nameLength * 2).decode('utf-16').rstrip('\x00')
            self.children = []
            for _ in range(self.childCount):
                self.children.append(ChildEntry(reader))

class FreeEntry:
        def __init__(self, entry: Entry, reader):
            self.next, = struct.unpack("q", reader.read(8))

def parseEntry(entry: Entry, reader):
    if entry.tag == "GGPK":
        return GGPKEntry(entry, reader)
    elif entry.tag == "FILE":
        return FileEntry(entry, reader)
    elif entry.tag == "PDIR":
        return PDirEntry(entry, reader)
    elif entry.tag == "FREE":
        return FreeEntry(entry, reader)

class GGPK:
    def __init__(self, reader):
        self.root = GGPKEntry(Entry(reader), reader)

    def render(self):
        print(RenderTree(self.tree, maxlevel=2))
        
    def index(self, reader):
        for rootOffset in self.root.offsets:
            reader.seek(rootOffset)
            topLevelEntry = parseEntry(Entry(reader), reader)
            if type(topLevelEntry) is PDirEntry and not topLevelEntry.name:
                topLevelEntry.name = "GGPK"
                self.tree = self.indexEntry(topLevelEntry, None, reader)
            
    def indexEntry(self, entry, parentNode: Node, reader):
        if type(entry) is PDirEntry:
            node = Node(entry.name, parent=parentNode)
            for child in entry.children:
                reader.seek(child.offset)
                childEntry = parseEntry(Entry(reader), reader)
                self.indexEntry(childEntry, node, reader)
            return node
        elif type(entry) is FileEntry:
            node = Node(entry.name, parent=parentNode)
            return node


