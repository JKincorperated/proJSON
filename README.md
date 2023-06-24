# proJSON

A python library to compress a dict into a bytearray.

[![Tests](https://github.com/The-Geiger-Network-Project/proJSON/actions/workflows/python-app.yml/badge.svg)](https://github.com/The-Geiger-Network-Project/proJSON/actions/workflows/python-app.yml)

## Install

``` sh

pip install proJSON

```

## The Crafter

### Types

``` python

# Format

"name" : {
    "type": type,      # Types specified below with arguments
    ...
}

"intExample" : {
    "type": "int",     # Set int type
    "byte": 1          # Set max int size to 1 byte (int8)
} 

"stringExample" : {
    "type": "string",  # Set string type
    "maxlen": 1        # Set max size of string ( the max size of the string is calculated by (2^(8*n)-1). if n is 1 then the max size is 255) (optional defaults to 2)
} 

"bytesExample" : {
    "type": "bytes",   # Set bytes type
    "maxlen": 1        # Set max size of string ( the max size of the string is calculated by (2^(8*n)-1). if n is 1 then the max size is 255) (optional defaults to 2)
} 

"dirExample" : {
    "type": "dir",     # Set dir type
    "subdirs": {}      # A dictionary of int, string and byte types in the format above.
} 

"boolExample" : {
    "type" : "bool"    # Set bool type
}

"listExample" : {
    "type" : "list",   # Set list type
    "subtype": "int",  # Set list contents type to an "int"
    "maxlen": 1        # The "maxlen" parameter for bytes or str (for "int" maxlen is still used instead of "byte")
}

```

***Don't put a dir in another dir. It won't work***

### Init

``` python

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
        "maxlen": 1
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

```

### Encoding data

``` python

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

print(encoded) # b'\x07\x0cHello World!\x00\rThis is bytes\xc8\x0cHello Again!' (43 bytes)

```

### Decoding data

``` python

data = b'\x07\x0cHello World!\x00\rThis is bytes\xc8\x0cHello Again!'

decoded = crafter.decode(data)

print(decoded) # {'intExample': 7, 'stringExample': 'Hello World!', 'bytesExample': b'This is bytes', 'dirExample': {'intExample2': 200, 'stringExample2': 'Hello Again!'}} (154 bytes)

```
