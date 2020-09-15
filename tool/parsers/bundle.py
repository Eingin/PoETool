from ..utils.oodle import OodleCompressionType
import struct
import ctypes



class BundleHeader:
     def __init__(self, reader):
        parsed = struct.unpack("IIQQIIIIII", reader.read(48))
        self.startCompressor = OodleCompressionType(parsed[0])
        self.uncompressedSize = parsed[2]
        self.payloadSize = parsed[3]
        self.chunkCount = parsed[4]
        self.chunkSize = parsed[5]

        self.chunkSizes = []
        for _ in range(self.chunkCount):
            self.chunkSizes.append(struct.unpack("I", reader.read(4)))
        
class GGGBundle:
    def __init__(self, reader):
        parsed = struct.unpack("III", reader.read(12))
        self.uncompressedSize = parsed[0]
        self.payloadSize = parsed[1]
        self.headerSize = parsed[2]
        self.header = BundleHeader(reader)

    def decompress(self, reader):
        try:
            from ..utils.oodle import OodLZDecompresss

            reader.seek(12 + self.headerSize)
            payloadBuffer = reader.read(self.payloadSize)
            compressedBuffer = (ctypes.c_ubyte * self.payloadSize).from_buffer_copy(payloadBuffer)
            self.decompressedBuffer = (ctypes.c_ubyte * self.uncompressedSize)()

            return OodLZDecompresss(
                compressedBuffer,
                 ctypes.c_size_t(self.payloadSize),
                  self.decompressedBuffer,
                   ctypes.c_size_t(self.uncompressedSize),
                    ctypes.c_int(0),
                    ctypes.c_int(0),
                    ctypes.c_int(0),
                    ctypes.POINTER(ctypes.c_ubyte)(),
                    ctypes.c_size_t(0),
                    ctypes.c_void_p(0),
                    ctypes.c_void_p(0),
                    ctypes.c_void_p(0),
                    ctypes.c_size_t(0),
                    ctypes.c_int(0)
                )
        except:
            return -1


