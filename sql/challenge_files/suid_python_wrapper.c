#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
    setreuid(1000, 1000);
    char command[100] = "/home/user/sql.py";
    system(command);
    return 0;
}
