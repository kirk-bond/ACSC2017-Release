# Do a byte for byte compare with the flag: acsc2017{arent_interpreters_great}
# r0 will be populated on entry with the guessed flag
# r0 should contain 0 on success on return

# Always execute the same number of instructions on success or failure to be
# resistant to dynamic instrumentation or instruction counting paired with brute
# force.

li r7 0     # r7 = success flag (stays 0 if each character matches the flag)
li r3 1     # r3 = xor key initial value
li r4 1     # r4 = addend to increment flag pointer and xor key

ld  r1 r0   # r1 = flag char
add r0 r4   # r0 = increment flag pointer
xor r1 r3   # r1 = crypted flag char
add r3 r4   # r3 = increment xor key
li  r2 0x60 # r2 = expected crypted flag char
xor r1 r2   # cmp
or  r7 r1   # Update r7 (success flag)

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x61
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x70
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x67
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x37
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x36
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x36
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x3f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x67
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x6c
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x34
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x6a
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x64
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x38
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x57
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x7f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x5d
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x5d
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x78
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x7a
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x7a
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x7f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x51
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x6b
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x6d
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x55
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x2e
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x6d
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x63
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r4
xor r1 r3
add r3 r4
li  r2 0x1f
xor r1 r2
or  r7 r1

mov r0 r7
