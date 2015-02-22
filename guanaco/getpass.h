#ifndef __GETPASS_H
#define __GETPASS_H
//#include<unistd.h>
#include<stdio.h>
#include<termios.h>
#include<string.h>
#include<unistd.h>

void getpasswd(char **user, size_t *userL, char **passwd, size_t *passL);
#endif
