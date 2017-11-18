#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void get_name() {
    fprintf(stdout, "Enter your name: ");

    char name_buff[255];
    gets(name_buff);

    fprintf(stdout, "Hello %s\n", name_buff);
}


int main(int argc, char **argv)
{
    setreuid(1000, 1000);
    get_name();
}
