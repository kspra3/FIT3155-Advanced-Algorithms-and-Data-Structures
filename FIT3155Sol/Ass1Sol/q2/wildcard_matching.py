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


def bad_character(string, length):
    # We obtain the occurrence of pattern for shifting.
    # Part of this code was obtained from geeksforgeeks.com

    # Initialize all occurrence as -1
    shift = [-1] * noOfChar

    # Fill the actual value of last occurrence
    for i in range(length):
        shift[ord(string[i])] = i

    # Return initialized list.
    # This is mainly pre-processing to know number of shifts.
    # Using linked list instead of a table.
    #print(shift)
    return shift


def good_prefix(string):
    # Gusfield's implementation.
    # We make it better using Galil's optimisation.
    # Part of this code was obtained from geeksforgeeks.com
    # Creating an array of zeros.
    good_prefix = [-1] * (len(string) + 1)
    # Pre-processing string.
    # Reversing.
    string = string[::-1]
    # Obtaining Z Array.
    z_array = zAlgo(string)
    # Reversing Z Arry
    z_array2 = z_array[::-1]

    for i in range(len(string)-1):
        j = len(string) - z_array2[i]
        good_prefix[j] = i

    return good_prefix


def wildcard_matching(text, pattern):
    # Mirrored BM used for pattern matching
    # Part of this code was obtained from geeksforgeeks.com

    # Assigning pattern length.
    M = len(pattern)
    # Assigning text length.
    N = len(text)
    i = N - M - 1#
    index = 1
    matches = []

    while i >= 0:
        shift = 0
        # Indexing the pattern match.
        j = 0
        while j < M and pattern[j] == text[i + j + 1]:
            j -= 1
        # When there's a match.
        if j == -1 or i + j - 1 == -1:
            # Index adjustment included.
            matches.append(i - j + index)
            # Shifting after match.
            i -= 1
        # When there's no match.
        # We compare the Bad Character and Good Prefix to know which yields a greater shift.
        # The one with a greater shift is followed.
        else:
            # Shift using Bad Character.
            bad_char_shift = max(1, j + bad_character(pattern, len(pattern))[ord(text[i + j - 1])])
            # Shift value using Good Prefix
            good_prefix_shift = 0
            #bComparing by Gusfield's implementation and Galil's optimisation.
            if (good_prefix(pattern))[j] == 0:
                good_prefix_shift = (matched_suffix(pattern)[j])

            elif (good_prefix(pattern))[j] > 0:
                good_prefix_shift = (good_prefix(pattern))[j]

            # Using the longest shift possible.
            shift = max(shift, bad_char_shift, good_prefix_shift)
            i -= shift

    return matches[::-1]


def matched_suffix(pattern):
    # For optimisation.
    # Part of this code was obtained from geeksforgeeks.com
    matches = zAlgo(pattern)
    j = 0
    for i in range(len(matches)-1, -1, -1):
        if matches[i] == len(pattern) - 1:
            j = max(j, matches[i])
        matches[i] = j

    return matches


def FileOutput(results):
    # Creating output file.
    f = open('output_wildcard_matching.txt', 'a')
    #Appending results onto file line by line.
    f.writelines("%s\n" % i for i in results)
    # Closing file.
    f.close()


def main():
    # Retrieving and processing files from command.
    text = ((open(sys.argv[1], "r")).read()).rstrip()
    pattern = ((open(sys.argv[2], "r")).read()).rstrip()
    # Running the algorithm.
    FileOutput(wildcard_matching(text, pattern))


if __name__ == "__main__":
    main()