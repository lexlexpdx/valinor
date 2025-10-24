// gcc -Wall ccwc -o ccwc

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define OPTIONS "c:l:w:m:"
#define BUFFER 50000

// Prototypes
void count_bytes(char *);
void count_lines(char *);


int main(int argc, char *argv[])
{

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
                {
                    count_bytes(optarg);
                    break;
                }
                case 'l':
                {
                    count_lines(optarg);
                    break;
                }
                default:
                    break;
            }
        }
    }

}


void count_bytes(char *file_name)
{
    FILE *file;
    char buffer[BUFFER];
    ssize_t num = 0;
    size_t total = 0;
    int fd;

    file = fopen(file_name, "r");

    if (file == NULL)
    {
        perror("empty file");
        exit(EXIT_FAILURE);
    }
    fd = fileno(file);
    while ((num = read(fd, buffer, BUFFER)) > 0)
    {
        total += num;
    }

    fclose(file);

    printf("%zu %s\n", total, optarg);

}


void count_lines(char *file_name)
{
    FILE *file;
    size_t total = 0;
    char c;

    file = fopen(file_name, "r");

    if (file == NULL)
    {
        perror("file is empty");
        exit(EXIT_FAILURE);
    }

    while ((c = fgetc(file)) != EOF)
    {
        if (c == '\n')
            ++total;
    }


    fclose(file);
    printf("%zu %s", total, file_name);

}