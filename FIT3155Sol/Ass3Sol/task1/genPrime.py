import sys
import random


def generate_prime(key):
    while True:
        # Using 2**k to include the range.
        # 2**(k-1) to (2**(k))-1
        number = random.randrange(2**(key-1), 2**key)
        # If the number generated is a Prime number, we return it.
        if check_prime(number):
            print(number)
            return number


def check_prime(number):
    # If number is less than 2 or number is even, return False.
    if number <= 1 or (number % 2 == 0):
        return False
    # Checking low Prime numbers.
    if number == 2 or number == 3:
        return True
    # Otherwise, RabinMiler is invoked.
    return rabin_miller(number)


def rabin_miller(n, loop=64):
    # Miller-Rabin's Randomized Primality testing algorithm.
    # Factor n- 1 as 2^s.t, where t is odd.
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    # Check if the number is composite or Prime.

    def composite(a, n):
        if pow(a, n - 1, n) == 1:
            return False
        for i in range(s + 1):
            if pow(a, 2 ** i * t, n) == n - 1:
                return False
        return True
    # At this stage n-1 will be 2^s.t, where t is odd.
    # k random tests.
    for _ in range(loop):
        # Choose a random number in [2..n-1)
        a = random.randrange(2, n - 1)
        if composite(a, n):
            return False
    return True


if __name__ == "__main__":
    # Main driver function.
    k = int(sys.argv[1])
    generate_prime(k)
