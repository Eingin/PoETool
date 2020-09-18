from ..utils.oodle import OodleCompressionType
import struct
import ctypes

class IndexBundleInfo:
     def __init__(self, reader):
        self.nameLen, = struct.unpack("I", reader.read(4))
        self.name = reader.read(self.nameLen).decode('utf-8')
        self.uncompressedSize, = struct.unpack("I", reader.read(4))

class IndexFileInfo:
     def __init__(self, reader):
        self.hash, self.bundleIndex, self.fileOffset, self.fileSize = struct.unpack("QIII", reader.read(20))

class IndexPathInfo:
     def __init__(self, reader):
        self.hash, self.payloadOffset, self.payloadSize, self.payloadRecursiveSize = struct.unpack("QIII", reader.read(20))

class BundleIndex:
     def __init__(self, reader):
        self.bundles = []
        self.files = dict()
        self.paths = dict()

        self.bundleCount, = struct.unpack("I", reader.read(4))
        for _ in range(self.bundleCount):
            self.bundles.append(IndexBundleInfo(reader))

        self.fileCount, = struct.unpack("I", reader.read(4))
        for _ in range(self.fileCount):
            info = IndexFileInfo(reader)
            self.files[info.hash] = info

        self.pathCount, = struct.unpack("I", reader.read(4))
        for _ in range(self.pathCount):
            path = IndexPathInfo(reader)
            self.paths[path.hash] = path

