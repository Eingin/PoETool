
def fnv64a( str ):
    hval = 0xcbf29ce484222325
    prime = 0x100000001B3
    uint64_max = 2 ** 64
    for s in str:
        hval = hval ^ ord(s)
        hval = (hval * prime) % uint64_max
    return hval