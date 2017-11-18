#!/usr/bin/env python3

"""
Encrypt a string using the same algorithm as harder.s

Xor the string with an incrementing xor key starting at 1.
"""

import argparse

def crypt(s):
    keystream = range(1, len(s)+1)
    return [ord(c) ^ k for c, k in zip(s, keystream)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("string", help="String to encrypt/decrypt")

    args = parser.parse_args()
    crypted = crypt(args.string + "\x00")
    print("".join(chr(c) for c in crypted))


if __name__ == "__main__":
    main()
