import zlib

class IDGenerator:
    last_call = 0

def generate_id():
    IDGenerator.last_call += 1
    return hex(zlib.crc32(bytes(str(IDGenerator.last_call), "ascii")) & 0xffffffff)[2:]
