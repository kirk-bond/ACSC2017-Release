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

  volatile int modify_me;
  char buffer[64];

  modify_me = 0;
  gets(buffer);

  if(modify_me != 0) {
      get_flag();
  } else {
      printf("Try again\n");
  }
}
