import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../src")) # Yes, it is hacky and Yes, it is not mine.

from proJSON import Crafter

def test_encode():
    template = {
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
            "maxlen": 2
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
                "bytesExample" : {
                    "type": "bytes",
                    "maxlen": 2
                },
            }
        },
        "boolExample" : {
            "type": "bool"
        },
        "listExample" : {
            "type": "list",
            "subtype": "int",
            "maxlen": 1 # the same as the "byte" field on the "intExample" field
        }
    }

    crafter = Crafter(template)

    exampledata = {
        "intExample" : 200,
        "stringExample" : "Hello World!",
        "bytesExample": b"This is bytes",
        "dirExample" : {
            "intExample2" : 201,
            "stringExample2": "Hello Again!",
            "bytesExample": b"Again, This is bytes"
        },
        "boolExample" : True,
        "listExample" : [1,2,3]
    }

    assert crafter.encode(exampledata) == b'\xc8\x0cHello World!\x00\rThis is bytes\xc9\x0cHello Again!\x00\x14Again, This is bytes\x01\x01\x02\x03\xff'

def test_decode():
    template = {
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
            "maxlen": 2
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
                "bytesExample" : {
                    "type": "bytes",
                    "maxlen": 2
                },
            }
        },
        "boolExample" : {
            "type": "bool"
        },
        "listExample" : {
            "type": "list",
            "subtype": "int",
            "maxlen": 1 # the same as the "byte" field on the "intExample" field
        }
    }

    crafter = Crafter(template)

    exampledata = {
        "intExample" : 200,
        "stringExample" : "Hello World!",
        "bytesExample": b"This is bytes",
        "dirExample" : {
            "intExample2" : 201,
            "stringExample2": "Hello Again!",
            "bytesExample": b"Again, This is bytes"
        },
        "boolExample" : True,
        "listExample" : [1,2,3]
    }

    x = crafter.encode(exampledata)

    assert crafter.decode(x) == exampledata