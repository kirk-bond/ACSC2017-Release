#include <stdio.h>

int main(int argc, char* argv[])
{
    if(argc == 2 && !strcmp("-h", argv[1]))
    {
        fprintf(stdout, "Usage: ./hello_world [-h]\n");
        return 0;
    }
    else if(argc == 2 && strcmp("-h", argv[1])) {
        fprintf(stdout, "Unknown argument\nUsage: ./hello_world [-h]\n");
        return -1;
    } 
    else if(argc > 2)
    {
        fprintf(stdout, "Too many arguments\n");
        exit(-1);
    } 
    fprintf(stdout, "Hello World!\n");
    return 0;
 }
