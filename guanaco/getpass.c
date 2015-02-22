#include"getpass.h"

//It is analog of getpass from <unistd.h>.
void getpasswd(char **user, size_t *userL, char **passwd, size_t *passL) {
	//int _in = fileno(stdin);
	//struct termios *settings = malloc(sizeof(struct termios)), *nsettings = malloc(sizeof(struct termios));
	size_t tmp = 0;
	//struct termios orig, noecho;
	*userL = 0; *passL = 0;
	*user = NULL; *passwd = NULL;
	printf("\n%d\n", *userL);
	printf("I'm GuANaCo's getpass, and I'm working!\n");
	printf("Login: ");
	if ((*userL = getline(user, &tmp, stdin)) < 0) {
		printf("All right!\n");
		perror("Something goes wrong.\n");
		return;
	}
	printf("%d %d\n", tmp, *userL);
	tmp = 0;
	printf("login %s\n", *user);
#if 0
	tcgetattr(_in, &orig);
	noecho = orig;
	noecho.c_lflag &= ~ECHO;
	tcsetattr(_in, TCSANOW, &noecho);
	printf("Password: ");
	if ((*passL = getline(passwd, &tmp, stdin)) < 0) {
		perror("Something goes wrong.\n");
		tcsetattr(_in, TCSANOW, &orig);
		return;
	}
	tcsetattr(_in, TCSANOW, &orig);
#endif
	*passwd = getpass("Password: ");
	printf("\n");
	printf("password %s\n", *user);
	printf("%d\n", (*user)[*userL - 1]);
	return;
}
