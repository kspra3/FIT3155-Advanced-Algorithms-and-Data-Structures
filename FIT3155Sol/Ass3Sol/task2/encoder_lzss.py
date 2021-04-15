"""
K. Sharsindra Pratheen
25636626
"""
# Parts of code obtained from geeksforgeeks.org and github.com
# Greatly modified them to follow assignment specifications and requirements.
# Majority of the concepts, implementations and pseudo-codes are from lectures and tutorials.

import sys
from collections import Counter
import elias_code
import huffman_code

def z_algo(string, index):
    # Implementing Z-algorithm.
    # Part of this code was obtained from geeksforgeeks.com
    m = len(string)
    # Initializing the array.
    z = [None] * m
    # [L,R] make a window which matches z box.
    left = right = 0

    for i in range(1, m):
        if i >= index:
            break
        # These are cases where there is no match.
        # Naive method used to calculate array.
        if i > right:
            left = right = i
            # Traversing from index 0.
            while right < m and string[right] == string[right - left]:
                right += 1
            z[i] = right - left
            right -= 1
        else:
            # Obtaining number of matches in the z box.
            j = i - left
            if z[j] < right - i + 1:
                z[i] = z[j]
            else:
                # Start from R and check manually.
                left = i
                while right < m and string[right - left] == string[right]:
                    right += 1
                z[i] = right - left
                right -= 1
    return z


class EncodeLZSS:
    # Given an input ASCII text file, search window size (integer) and lookahead buffer size (integer) L
    # Return a binary stream of bits
    # Implementing Lempel-Ziv-Storer-Szymanski (LZSS) variation of LZ77 algorithm with specifications.
    # Initialising the variables.
    def __init__(self, string, search_window, lookahead_buffer):
        self.string = string
        self.search_window = search_window
        self.lookahead_buffer = lookahead_buffer
        self.huffman_ = huffman_code.values(string)[0]

    def encode(self):
        # Concatenating the header and data part for the output.
        # Return a binary stream of bits
        binary = self.header_part()
        binary += self.data_part()
        return binary

    def header_part(self):
        # The Header encoding of the string.
        # Encoding the number of unique ASCII characters in the input text using variable-length Elias code.
        # Fixed-length 7-bit ASCII code.
        # Then length of the Huffman code assigned to that unique character is encoded and appended.
        header = ""
        unique = list(Counter(self.string))
        unique.sort()
        header += elias_code.encoder(len(unique))

        for i in unique:
            # Fixed-length 7-bit ASCII code.
            header += "{0:0=7d}".format(int(bin(ord(i))[2:]))
            # Encoding the number of unique ASCII characters in the input text using variable-length Elias code.
            header += elias_code.encoder(len(self.huffman_[i]))
            # Then length of the Huffman code assigned to that unique character is encoded and appended.
            header += huffman_code.values(self.string)[0][i]
        return header

    def data_part(self):
        # The Data encoding of the string.
        # Encoding the variable-length Elias code, the total number of Format-0 and Format-1 fields.
        data = ""
        lzss = EncodeLZSS.encoder(self)
        data += elias_code.encoder(len(lzss))

        for i in lzss:
            if i[0] == 0:
                # Format-0,
                # Offset and length are each encoded using the variable-length Elias code.
                data += "0"
                data += elias_code.encoder(i[1])
                data += elias_code.encoder(i[2])
            else:
                # Format-1
                # Character is encoded using its assigned variable-length Huffman code defined in the header.
                data += "1"
                data += self.huffman_[i[1]]
        return data

    def encoder(self):
        i = 0
        lzss = []
        while i < len(self.string):
            lzss.append(self.encode_single(i))
            if (self.encode_single(i))[0] == 1:
                i += 1
            else:
                i += (self.encode_single(i))[2]
        return lzss

    def encode_single(self, index):
        # Initialising the lookahead buffer and the search window.
        lookahead_buffer = self.string[index: index + self.lookahead_buffer]
        search_window = self.string[max(0, index - self.search_window): index]
        # Generating the longest prefixes of all matches using the z-algorithm.
        z_arr = z_algo(f"{lookahead_buffer} {search_window}{lookahead_buffer}", len(lookahead_buffer) + 1 + len(search_window))
        try:
            # Handling cases when there are no matches.
            if z_arr[self.lookahead_buffer + 1] is None:
                return 1, self.string[index]
            # Handling cases when there are matches.
            else:
                # The longest prefix and where to begin.
                # Removing all occurrences of None.
                length = max(list(filter(None.__ne__, z_arr[self.lookahead_buffer + 1:])))
                if length is not None and length >= 3:
                    return 0, (len(lookahead_buffer) + 1 + len(search_window) - (z_arr[self.lookahead_buffer + 1:]).index(length) - self.lookahead_buffer - 1), length
                else:
                    return 1, self.string[index]
        except IndexError:
            return 1, self.string[index]


def main():
    # Retrieving and processing files from command.
    text_file = open(sys.argv[1], "rb").read().decode()
    search_window = int(sys.argv[2])
    lookahead_buffer = int(sys.argv[3])
    encode = (EncodeLZSS(text_file, search_window, lookahead_buffer)).encode()
    # Printing the values to the output file.
    output_file = open("output_encoder_lzss.bin", "w")
    output_file.write(encode)
    #print(encode)
    output_file.close()


if __name__ == "__main__":
    # Main driver function.
    main()
