class crafter:
    def __init__(self, protoJSON):
        self.protoJSON = protoJSON

    def decode(self, data: bytes):
        ret = {}
        offset = 0
        for k, v in self.protoJSON.items():
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
        
        return ret


    def encode(self, data: dict):
        ret = b""
        for k, v in self.protoJSON.items():
            item = data[k]
            if v["type"] == "int":
                ret += int.to_bytes(item, v["byte"], "big")
            elif v["type"] == "string":
                maxlen = v["maxlen"] if "maxlen" in v else 2
                bytestr = item.encode()
                ret += int.to_bytes(len(bytestr), maxlen, "big")
                ret += bytestr
            elif v["type"] == "bytes":
                maxlen = v["maxlen"] if "maxlen" in v else 2
                ret += int.to_bytes(len(item), maxlen, "big")
                ret += item
            elif v["type"] == "dir":
                for subk, subv in v["subdirs"].items():
                    subitem = data[k][subk]
                    if subv["type"] == "int":
                        ret += int.to_bytes(subitem, subv["byte"], "big")
                    elif subv["type"] == "string":
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        bytestr = subitem.encode()
                        ret += int.to_bytes(len(bytestr), maxlen, "big")
                        ret += bytestr
                    elif subv["type"] == "bytes":
                        maxlen = subv["maxlen"] if "maxlen" in subv else 2
                        ret += int.to_bytes(len(subitem), maxlen, "big")
                        ret += subitem
        return ret