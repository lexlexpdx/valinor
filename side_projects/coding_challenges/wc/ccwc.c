// gcc -Wall ccwc -o ccwc

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define OPTIONS "c:l:w:m:"
#define BUFFER 50000


int main(int argc, char *argv[])
{
    FILE *file;
    char buffer[BUFFER];
    ssize_t num;
    size_t total = 0;
    int fd;

    if (argc < 2)
    {
        printf("Must give a value on the command line\n");
        exit(EXIT_FAILURE);
    }

    {
        int opt = 0;

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            switch (opt)
            {
                case 'c':
                    file = fopen(optarg, "r");
                    if (file == NULL)
                    {
                        perror("Error opening file");
                        exit(EXIT_FAILURE);
                    }
                    fd = fileno(file);
                    while ((num = read(fd, buffer, BUFFER)) > 0)
                    {
                        total += num;
                    }
                    printf("%zu %s\n", total, optarg);
                default:
                    break;
            }
        }
    }

}