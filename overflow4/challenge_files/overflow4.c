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

void get_input() {
  char buffer[255];
  gets(buffer);

  printf("Try again\n");
}

int main(int argc, char **argv)
{
  setreuid(1000, 1000);
  get_input();
}
