#!/usr/bin/env python3

"""
Assemble into binary code and generate a header file that defines the `CODE`
array.

The custom architecture supports 6 instructions:
li  reg1 imm    - Load imm value into reg1
ld  reg1 reg2   - Load the contents at address reg2 into reg1
mov reg1 reg2   - mov reg2 into reg1
add reg1 reg2   - add reg1 and reg2, store result in reg1
xor reg1 reg2   - xor reg1 and reg2, store result in reg1
or  reg1 reg2   - or reg1 and reg2, store result in reg1

General purpose registers r0-r7 are supported and immediates can be in base 10
or 16 (0x prefix).
"""

import argparse

def print_c_header(code):
    print("const unsigned char CODE[{:d}] = {{".format(len(code)))
    lines = [code[i:i+8] for i in range(0, len(code), 8)]
    for line in lines:
        print("    " + ", ".join("0x{:02x}".format(ord(c)) for c in line) + ",")
    print("};")


def parse_reg(reg):
    assert(reg.startswith("r") and len(reg) == 2)
    return chr(int(reg[1]))


def parse_imm(imm):
    try:
        return chr(int(imm))
    except:
        return chr(int(imm, 16))


def assemble(lines):
    code = ""
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        ops = line.split()
        if ops[0] == "li":
            code += "\x61"
            code += parse_reg(ops[1])
            code += parse_imm(ops[2])
        elif ops[0] == "ld":
            code += "\x62"
            code += parse_reg(ops[1])
            code += parse_reg(ops[2])
        elif ops[0] == "mov":
            code += "\x63"
            code += parse_reg(ops[1])
            code += parse_reg(ops[2])
        elif ops[0] == "add":
            code += "\x64"
            code += parse_reg(ops[1])
            code += parse_reg(ops[2])
        elif ops[0] == "xor":
            code += "\x65"
            code += parse_reg(ops[1])
            code += parse_reg(ops[2])
        elif ops[0] == "or":
            code += "\x66"
            code += parse_reg(ops[1])
            code += parse_reg(ops[2])
        else:
            raise RuntimeError("Unsupprted instruction")

    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Assembly file to parse")

    args = parser.parse_args()
    with open(args.file, "r") as f:
        data = f.read()

    code = assemble([l.strip() for l in data.split("\n")])
    print_c_header(code)


if __name__ == "__main__":
    main()
