#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

void get_flag() {
  FILE *fp;
  char buff[255];
  fp = fopen("/home/user/flag", "r");
  fscanf(fp, "%s", buff);
  printf("%s\n", buff);
  fclose(fp);
}


int main(int argc, char **argv)
{
  setreuid(1000, 1000);

  volatile int (*function_pointer)();
  volatile int modify_me;
  char buffer[64];

  modify_me = 0;
  function_pointer = 0;
  gets(buffer);

  if(modify_me == 0x61637363) {
      if(function_pointer) {
          printf("Calling function_pointer, jumping to 0x%08x\n", function_pointer);
          function_pointer();
      }
      else {
          printf("function_pointer is still 0\n");
      }
  } else {
      printf("Try again\n");
  }
}
