import zlib
import struct

def compress(data, compression_level=-1):
    compressed = zlib.compress(data, level=compression_level)
    header = struct.pack('>I', len(data))
    return header + compressed

def uncompress(data):
    data = zlib.decompress(data[4:]).decode('utf-8')
    return data
