from lz4 import frame
from zlib import compress, decompress
from math import floor

class Crafter:
    def __init__(self, proJSON, compression="lz4"):
        self.proJSON = proJSON
        if compression != "lz4" and compression != "zlib" and compression != "dev":
            print(f"The compression type {self.compression} is not supported. The current options are lz4, zlib and dev (no compression)")
            print("If you believe this is an error, please submit a bug report at https://github.com/The-Geiger-Network-Project/proJSON/issues")
            print("Defaulting to lz4 compression")
            self.compression = "lz4"
        else:
            self.compression = compression

    def decode(self, data: bytes):

        if self.compression == "zlib":
            data = decompress(data)
        elif self.compression == "lz4":
            if len(data) > 256:
                context = frame.create_decompression_context()
                decompressed = b""
                for i in range(floor(len(data) / 256)):
                    decompressed += frame.decompress_chunk(context, data[i*256:(i+1)*256])
                decompressed += frame.decompress_chunk(context, data[floor(len(data) / 256):floor(len(data) / 256)+(len(data) % 256)])
            else:
                decompressed = frame.decompress(data)
                
            data = decompressed

        ret = {}
        offset = 0
        for k, v in self.proJSON.items():
            if v["type"] == "int":
                ret[k] = int.from_bytes(data[offset:offset+v["byte"]], "big")
                offset += v["byte"]
            elif v["type"] == "string":
                maxlen = v["maxlen"] if "maxlen" in v else 2
                length = int.from_bytes(data[offset:offset+maxlen], "big")
                offset += maxlen
                bytestr = data[offset:offset+length]
                ret[k] = bytestr.decode()
                offset += length
            elif v["type"] == "bytes":
                maxlen = v["maxlen"] if "maxlen" in v else 2
                length = int.from_bytes(data[offset:offset+maxlen], "big")
                offset += maxlen
                ret[k] = data[offset:offset+length]
                offset += length
            elif v["type"] == "dir":
                subret = {}
                for subk, subv in v["subdirs"].items():
                    if subv["type"] == "int":
                        subret[subk] = int.from_bytes(data[offset:offset+subv["byte"]], "big")
                        offset += subv["byte"]
                    elif subv["type"] == "string":
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        length = int.from_bytes(data[offset:offset+maxlen], "big")
                        offset += maxlen
                        bytestr = data[offset:offset+length]
                        subret[subk] = bytestr.decode()
                        offset += length
                    elif subv["type"] == "bytes":
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        length = int.from_bytes(data[offset:offset+maxlen], "big")
                        offset += maxlen
                        subret[subk] = data[offset:offset+length]
                        offset += length
                ret[k] = subret
            elif v["type"] == "bool":
                ret[k] = bool(data[offset])
                offset += 1
            elif v["type"] == "list":
                maxlen = v["maxlen"] if "maxlen" in v else 2
                subret = []
                while True:
                    if data[offset] == 255:
                        break
                    if v["subtype"] == "int":
                        subret.append(int.from_bytes(data[offset:offset+maxlen], "big"))
                        offset += maxlen
                    elif v["subtype"] == "string":
                        length = int.from_bytes(data[offset:offset+maxlen], "big")
                        offset += maxlen
                        bytestr = data[offset:offset+length]
                        subret.append(bytestr.decode())
                        offset += length
                    elif v["subtype"] == "bytes":
                        length = int.from_bytes(data[offset:offset+maxlen], "big")
                        offset += maxlen
                        subret.append(data[offset:offset+length])
                        offset += length
                    elif v["subtype"] == "bool":
                        subret.append(bool(data[offset]))
                        offset += 1
                    
                ret[k] = subret
        return ret


    def encode(self, data: dict):
        ret = b""
        for k, v in self.proJSON.items():
            item = data[k]
            if v["type"] == "int":
                if isinstance(item, int):
                    pass
                else:
                    raise InvalidType(f"{str(item)} is supposed to be an int, but it's a {str(type(item))}")
                ret += int.to_bytes(item, v["byte"], "big")
            elif v["type"] == "string":
                if isinstance(item, str):
                    pass
                else:
                    raise InvalidType(f"{str(item)} is supposed to be a str, but it's a {str(type(item))}")
                maxlen = v["maxlen"] if "maxlen" in v else 2
                bytestr = item.encode()
                ret += int.to_bytes(len(bytestr), maxlen, "big")
                ret += bytestr
            elif v["type"] == "bytes":
                if isinstance(item, bytes):
                    pass
                else:
                    raise InvalidType(f"{str(item)} is supposed to be bytes, but it's a {str(type(item))}")
                maxlen = v["maxlen"] if "maxlen" in v else 2
                ret += int.to_bytes(len(item), maxlen, "big")
                ret += item
            elif v["type"] == "dir":
                if isinstance(item, dict):
                    pass
                else:
                    raise InvalidType(f"{str(item)} is supposed to be dict, but it's a {str(type(item))}")
                for subk, subv in v["subdirs"].items():
                    subitem = data[k][subk]
                    if subv["type"] == "int":
                        if isinstance(subitem, int):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} is supposed to be an int, but it's a {str(type(item))}")
                        ret += int.to_bytes(subitem, subv["byte"], "big")
                    elif subv["type"] == "string":
                        if isinstance(subitem, str):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} is supposed to be a str, but it's a {str(type(item))}")
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        bytestr = subitem.encode()
                        ret += int.to_bytes(len(bytestr), maxlen, "big")
                        ret += bytestr
                    elif subv["type"] == "bytes":
                        if isinstance(subitem, bytes):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} is supposed to be bytes, but it's a {str(type(item))}")
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        ret += int.to_bytes(len(subitem), maxlen, "big")
                        ret += subitem
            elif v["type"] == "bool":
                if isinstance(item, bool):
                    pass
                else:
                    raise InvalidType(f"{str(item)} is supposed to be bool, but it's a {str(type(item))}")
                ret += b"\x01" if item else b"\x00"
            elif v["type"] == "list":
                for i in item:
                    if v["subtype"] == "int":
                        if isinstance(i, int):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} contains an invalid item : {str(type(item))}")
                        
                        ret += int.to_bytes(i, v["maxlen"], "big")

                    if v["subtype"] == "bytes":
                        if isinstance(i, bytes):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} contains an invalid item : {str(type(item))}")
                        
                        ret += int.to_bytes(len(i), v["maxlen"], "big")
                        ret += i

                    if v["subtype"] == "string":
                        if isinstance(i, str):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} contains an invalid item : {str(type(item))}")
                        
                        ret += int.to_bytes(len(i.encode("utf-8")), v["maxlen"], "big")
                        ret += i.encode("utf-8")

                    if v["subtype"] == "bool":
                        if isinstance(i, bool):
                            pass
                        else:
                            raise InvalidType(f"{str(item)} contains an invalid item : {str(type(item))}")
                        
                        ret += b"\x01" if i else b"\x00"

                ret += b"\xff"

        if self.compression == "zlib":
            ret = compress(ret)
        elif self.compression == "lz4":
            if len(ret) > 256:
                context = frame.create_compression_context()
                compressed = frame.compress_begin(context)
                for i in range(floor(len(ret) / 256)):
                    compressed += frame.compress_chunk(context, ret[i*256:(i+1)*256])
                compressed += frame.compress_chunk(context, ret[floor(len(ret) / 256):floor(len(ret) / 256)+(len(ret) % 256)])
                compressed += frame.compress_flush(context)
            else:
                compressed = frame.compress(ret)
                
            ret = compressed
                        
        return ret
    

class InvalidType(BaseException):
    pass