from enum import Enum
import ctypes

from termcolor import cprint, colored

class OodleCompressionType(Enum):
    Unknown = 0
    Kraken = 8
    Mermaid = 9
    Leviathan = 13

# Load oodle DLL
try:
    oodleDll = ctypes.WinDLL("oo2core_7_win64.dll")

    OodLZCompressFuncProto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # return
        ctypes.c_int,      # codec
        ctypes.POINTER(ctypes.c_ubyte),   # src_buf
        ctypes.c_size_t,   # src_len
        ctypes.POINTER(ctypes.c_ubyte),   # dst_buf
        ctypes.c_int,      # level
        ctypes.c_void_p,   # opts
        ctypes.c_size_t,   # offs
        ctypes.c_size_t,   # unused
        ctypes.c_void_p,   # scratch
        ctypes.c_size_t,   # scratch_size
    ) 

    compress_paramflags = (1, 'codec', 0), (1, 'src_buf', 0), (1, 'src_len', 0), (1, 'dst_buf', 0), (1, 'level', 0), (1, 'opts', 0), (1, 'offs', 0), (1, 'unused', 0), (1, 'scratch', 0), (1, 'scratch_size', 0)

    OodLZCompress = OodLZCompressFuncProto(("OodleLZ_Compress", oodleDll), compress_paramflags)

    OodLZDecompressFuncProto = ctypes.WINFUNCTYPE (
        ctypes.c_int,      # return
        ctypes.POINTER(ctypes.c_ubyte),   # src_buf
        ctypes.c_size_t,   # src_len
        ctypes.POINTER(ctypes.c_ubyte),   # dst
        ctypes.c_size_t,   # dst_size
        ctypes.c_int,      # fuzz
        ctypes.c_int,      # crc
        ctypes.c_int,      # verbose
        ctypes.POINTER(ctypes.c_ubyte),   # dst_base
        ctypes.c_size_t,   # e
        ctypes.c_void_p,   # cb
        ctypes.c_void_p,   # cb_ctx
        ctypes.c_void_p,   # scratch
        ctypes.c_size_t,   # scratch_size
        ctypes.c_int,      # threadPhase
    )

    decompress_paramFlags = (1, "src_buf", 0), (1, "src_len", 0), (1, "dst", 0), (1, "dst_size", 0), (1, "fuzz", 0), (1, "crc", 0), (1, "verbose", 0), (1, "dst_base", 0), (1, "e", 0), (1, "cb", 0), (1, "cb_ctx", 0), (1, "scratch", 0), (1, "scratch_size", 0), (1, "threadPhase", 0)

    OodLZDecompresss = OodLZDecompressFuncProto(("OodleLZ_Decompress", oodleDll), decompress_paramFlags)
except:
    cprint(colored("WARNING: Unable to load Oddle. You will not be able to decompress bundles", "yellow"))