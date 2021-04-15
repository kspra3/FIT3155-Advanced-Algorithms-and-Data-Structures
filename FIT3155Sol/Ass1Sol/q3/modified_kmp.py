# K. Sharsindra Pratheen
# 25636626

import sys

noOfChar = 256


def zAlgo(string):
    # Implementing Z-algorithm.
    # Part of this code was obtained from geeksforgeeks.com
    m = len(string)
    # Initializing the array.
    z = [None] * m
    # [L,R] make a window which matches z box.
    L = R = j = 0

    for i in range(1, m):
        # These are cases where there is no match.
        # Naive method used to calculate array.
        if i > R:
            L = R = i
            # Traversing from index 0.
            while R < m and string[R - L] == string[R]:
                R += 1
            z[i] = R - L
            R -= 1
        else:
            # Obtaining number of matches in the z box.
            j = i - L
            if z[j] < R - i + 1:
                z[i] = z[j]
            else:
                # Start from R and check manually.
                L = i
                while R < m and string[R - L] == string[R]:
                    R += 1
                z[i] = R - L
                R -= 1
    return z


def modified_kmp(text, pattern):
    # Implementing a modified version of the Knuth-Morris-Pratt Algorithm.
    # Part of this code was obtained from geeksforgeeks.com and Github.com

    M = len(pattern)
    N = len(text)

    # Index for text.
    i = 0
    index = 1
    matches = []

    while i <= N - M:

        shift = 0
        j = 0

        # Loops to calculate until M - 1.
        while j < M and pattern[j] == text[i + j]:
            j += 1

        # Mismatch after j matches.
        if j != M:
            # Doesn't match the array characters,
            k = text[i + j]
            if j > 0:
                shift = j - longestSP(pattern)[M - 1]
            else:
                shift = 1
        else:
            # Match found, shift using longestSP.
            matches.append(i + index)
            shift = M - longestSP(pattern)[M - 1]

        i += max(shift, 1)

    return matches


def longestSP(pattern):
    # Part of this code was obtained from geeksforgeeks.com and Github.com
    M = len(pattern)
    # Creating array that will hold the longest SP.
    SP = [0] * M
    # Processing the Z Array.
    z = zAlgo(pattern)

    for i in range(M - 1, 1):
        j = i + z[i] - 1
        SP[j] = z[i]
    return SP


def FileOutput(results):
    # Creating output file.
    f = open('output_kmp.txt', 'a')
    # Appending results onto file line by line.
    f.writelines("%s\n" % i for i in results)
    # Closing file.
    f.close()


def main():
    # Retrieving and processing files from command.
    text = ((open(sys.argv[1], "r")).read()).rstrip()
    pattern = ((open(sys.argv[2], "r")).read()).rstrip()
    # Running the algorithm.
    FileOutput(modified_kmp(text, pattern))


if __name__ == "__main__":
    main()
