#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
    setreuid(1000, 1000);
    char command[100] = "/home/user/hello_world";
    if(argc == 2)
    {
        char *arg1 = argv[1];
        char *space = " ";
        strcat(command, space);
        strcat(command, arg1);
    }
    if(argc > 2)
    {
        fprintf(stdout, "Too many arguments\n");
        exit(-1);
    }

    fprintf(stdout, "Running: %s\n", command);
    system(command);
    return 0;
 }
