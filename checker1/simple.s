# Do a byte for byte compare with the flag: acsc2017{arent_interpreters_great}
# r0 will be populated on entry with the guessed flag
# r0 should contain 0 on success on return

# Always execute the same number of instructions on success or failure to be
# resistant to dynamic instrumentation or instruction counting paired with brute
# force.

li r7 0     # r7 = success flag (stays 0 if each character matches the flag)
li r3 1     # r3 = addend to increment flag pointer

ld  r1 r0   # r1 = flag char
add r0 r3   # r0 = increment flag pointer
li  r2 0x61 # r2 = expected flag char
xor r1 r2   # cmp
or  r7 r1   # Update r7 (success flag)

ld  r1 r0
add r0 r3
li  r2 0x63
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x73
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x63
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x32
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x30
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x31
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x37
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x7b
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x61
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x65
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x6e
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x74
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x5f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x69
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x6e
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x74
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x65
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x70
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x65
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x74
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x65
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x73
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x5f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x67
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x72
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x65
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x61
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x74
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x3f
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x7d
xor r1 r2
or  r7 r1

ld  r1 r0
add r0 r3
li  r2 0x00
xor r1 r2
or  r7 r1

mov r0 r7
