"""
K. Sharsindra Pratheen
25636626
"""


# Parts of code obtained from geeksforgeeks.org and github.com
# Greatly modified them to follow assignment specifications and requirements.
# Majority of the concepts, implementations and pseudo-codes are from lectures and tutorials.

def encode(values):
    # Encoding the number of unique ASCII characters in the input text using variable-length Elias code.
    result = ""
    for number in values:
        result += encoder(number)

    return len(values), result


def encoder(values):
    # Encoding the number of unique ASCII characters in the input text using variable-length Elias code.
    valuelist = []
    length = len(bin(values)[2:]) - 1
    while length > 1:
        codelength = bin(length)[2:]
        codelist = list(codelength)
        codelist[0] = "0"
        codelength = "".join(codelist)
        valuelist.append(codelength)
        length = len(codelength) - 1

    if values >= 2:
        valuelist.append("0")
        valuelist.reverse()
    return "".join(valuelist) + bin(values)[2:]


def decode(encoded):
    # Decoding the length of the variable-length Elias code.
    decoded = []
    for i in encoded:
        decoded.append(decoder(i))
    return decoded


def decoder(encoded):
    # Decoding the length of the variable-length Elias code.
    length = int("1", 2)
    pointer = 0
    while True:
        code = encoded[pointer: pointer + length]
        if code[0] == "1":
            return int(code[:len(code)], 2)
        else:
            codelist = list(code)
            codelist[0] = "1"
            code = "".join(codelist)
            pointer = pointer + length
            length = int(code, 2) + 1
