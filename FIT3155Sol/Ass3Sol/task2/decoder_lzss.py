"""
K. Sharsindra Pratheen
25636626
"""
# Parts of code obtained from geeksforgeeks.org and github.com
# Greatly modified them to follow assignment specifications and requirements.
# Majority of the concepts, implementations and pseudo-codes are from lectures and tutorials.

import sys
import elias_code


huffman_code = {}

def decode_lzss(binary):
    # Decoding the header back into ASCII characters.
    uniques = elias_code.decoder(binary)
    split = elias_code.encoder(uniques)
    binary = binary[len(split):]
    for i in range(uniques):
        # Decoding the fixed-length 7-bit ASCII code.
        # Unique characters.
        chars = chr(int(binary[0:7], 2))
        binary = binary[7:]
        # Decoding the length of the variable-length Elias code.
        # Decoding the length of the Huffman code.
        huffman_length = elias_code.decoder(binary)
        split = elias_code.encoder(huffman_length)
        binary = binary[len(split):]
        huffman = binary[0:huffman_length]
        binary = binary[huffman_length:]
        huffman_code[chars] = huffman

    # Decoding the data part back into ASCII characters.
    lzss_count = elias_code.decoder(binary)
    binary = binary[len(elias_code.encoder(lzss_count)):]
    encoded_lzss = []
    for i in range(lzss_count):
        # Checking the initial bit of the encoding.
        bit = int(binary[0])
        binary = binary[1:]
        if bit == 0:
            # Decoding the offset
            shift = elias_code.decoder(binary)
            binary = binary[len(elias_code.encoder(elias_code.decoder(binary))):]
            # Decoding the length of the code.
            length = elias_code.decoder(binary)
            binary = binary[len(elias_code.encoder(elias_code.decoder(binary))):]
            encoded_lzss.append((0, shift, length))
        elif bit == 1:
            char, huffman = characters(binary)
            binary = binary[len(huffman):]
            encoded_lzss.append((1, char))
    decoded_lzss = ""
    # Decoding the lzss code.
    for i in encoded_lzss:
        if i[0] == 1:
            decoded_lzss += i[1]
            continue
        elif i[0] == 0:
            string = decoded_lzss[len(decoded_lzss) - i[1] : len(decoded_lzss)]
            string = (string * (int(i[2] / len(string)) + 1))[:i[2]]
            decoded_lzss += string
    return decoded_lzss


def characters(binary):
    values = huffman_code.values()
    for i in values:
        matches = True
        for j in range(len(i)):
            if binary[j] != i[j]:
                matches = False
                break
        if matches != True:
            continue
        for k, l in huffman_code.items():
            if l == i:
                return k, l
    raise Exception


def main():
    # Retrieving and processing files from command.
    #file = sys.argv[1]
    #file = "output_encoder_lzss.bin"
    #text_file = open(file, "rb").read().decode("utf-8")
    f = open(sys.argv[1], "rb").read()
    text_file = f.decode("utf-8")
    decode = decode_lzss(str(text_file))
    # Printing the values to the output file.
    output_file = open("output_decoder_lzss.txt", "w")
    output_file.write(decode)
    # print(decode)
    output_file.close()


if __name__ == "__main__":
    # Main driver function.
    main()
