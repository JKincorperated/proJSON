from proJSON import Crafter
import random

def crafterTest():
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
                "bytesExample" : {
                    "type": "bytes",
                    "byte": 1
                },
            }
        } 
    }

    crafter = Crafter(template)


def encodeTest():
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
                "bytesExample" : {
                    "type": "bytes",
                    "byte": 1
                },
            }
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
        }
    }

    assert crafter.encode(exampledata) == b'\xc8\x0cHello World!\x00\rThis is bytes\xc9\x0cHello Again!\x00\x14Again, This is bytes'

def decodeTest():
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
                "bytesExample" : {
                    "type": "bytes",
                    "byte": 1
                },
            }
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
        }
    }

    x = crafter.encode(exampledata)

    assert crafter.decode(x) == exampledata