from proJSON import Crafter

template = {
    # See the [types section](###Types) for how to make this.
    "intExample" : {
        "type": "int",
        "byte": 1
    },
    "stringExample" : {
        "type": "string",
        "maxlen": 1
    },
    "bytesExample" : {
        "type": "bytes",
        "byte": 1
    },
    "dirExample" : {
        "type": "dir",
        "subdirs": {
            "intExample2" : {
                "type": "int",
                "byte": 1
            },
            "stringExample2" : {
                "type": "string",
                "maxlen": 1
            },
        }
    } 
}

crafter = Crafter(template)

exampledata = {
    "intExample" : 7,
    "stringExample" : "Hello World!",
    "bytesExample": b"This is bytes",
    "dirExample" : {
        "intExample2" : 200,
        "stringExample2": "Hello Again!"
    }
}

encoded = crafter.encode(exampledata)

print(encoded)

data = b'\x07\x0cHello World!\x00\rThis is bytes\xc8\x0cHello Again!'

decoded = crafter.decode(data)

print(decoded)
