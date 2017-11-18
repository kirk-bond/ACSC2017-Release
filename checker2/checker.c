#include "harder.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum opcodes {
    OP_LI = 0x61,   // reg, imm
    OP_LD,          // reg, [reg]
    OP_MOV,         // reg, reg
    OP_ADD,         // reg, reg
    OP_XOR,         // reg, reg
    OP_OR,          // reg, reg
//    OP_JMP,         // off
//    OP_JE,          // reg, reg, off
//    OP_JNE,         // reg, reg, off
} opcodes;


int check_flag(char *flag)
{
    // Initialize reg's one by one since it results in less optimized code and
    // makes it easier for users to realize each register location is a distinct
    // local variable.
    // Initialize r0 with a pointer to the guessed flag.
    // int regs[8] = {(int)flag, 0, 0, 0, 0, 0, 0, 0};
    int regs[8];
    regs[0] = (int)flag;
    regs[1] = 0;
    regs[2] = 0;
    regs[3] = 0;
    regs[4] = 0;
    regs[5] = 0;
    regs[6] = 0;
    regs[7] = 0;

    // I would use a switch here, but that makes the resulting object code a
    // little more difficult than I'd like for this problem.
    for (int i = 0; i < sizeof(CODE); i += 3) {
        unsigned char opcode = CODE[i];
        int op1 = CODE[i+1];
        int op2 = CODE[i+2];
        if (opcode == OP_LI) {
            regs[op1] = op2;
        }
        else if (opcode == OP_LD) {
            regs[op1] = *((char *)regs[op2]);
        }
        else if (opcode == OP_MOV) {
            regs[op1] = regs[op2];
        }
        else if (opcode == OP_ADD) {
            regs[op1] += regs[op2];
        }
        else if (opcode == OP_XOR) {
            regs[op1] ^= regs[op2];
        }
        else if (opcode == OP_OR) {
            regs[op1] |= regs[op2];
        }
        else {
            return -1;
        }
    }

    // Return code should be stored in r0
    return regs[0];
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <flag>\n", argv[0]);
        exit(-1);
    }

    // Copy to a separate buffer so we don't give a competitor any hints about
    // how long the flag is. They will have to examine the custom assembly to
    // figure that out.
    char buf[40];
    memset(buf, 0, sizeof(buf));
    strncpy(buf, argv[1], sizeof(buf));

    if (!check_flag(buf)) {
        printf("You win!\n");
        return 0;
    }

    printf("fail :(\n");
    return -1;
}
