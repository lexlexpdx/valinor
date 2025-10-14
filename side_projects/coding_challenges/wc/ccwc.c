// gcc -Wall ccwc -o ccwc

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define OPTIONS "clwm"


int main(int argc, char *argv[])
{
    FILE *file;
    int bytes = 0;

    if (argc < 2)
    {
        printf("Must give a value on the command line\n");
        exit(EXIT_FAILURE);
    }

    {
        int opt = 0;

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            swtich (opt)
            {
                case 'c':
                    file = fopen(optarg, )
            }
        }
    }

}