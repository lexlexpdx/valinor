// gcc -Wall ccwc -o ccwc

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <stdbool.h>

#define OPTIONS "c:l:w:m:"
#define BUFFER 50000

// Prototypes
void count_bytes(char *);
void count_lines(char *, bool is_default);
void count_words(char *, bool is_default);
void count_chars(char *);


int main(int argc, char *argv[])
{

    bool option_found = false;
    bool is_default = false;
    int opt;

    if (argc < 2)
    {
        printf("Must give a value on the command line\n");
        exit(EXIT_FAILURE);
    }


    while ((opt = getopt(argc, argv, OPTIONS)) != -1)
    {
        option_found = true;
        switch (opt)
        {
            case 'c':
            {
                count_bytes(optarg);
                break;
            }
            case 'l':
            {
                count_lines(optarg, is_default);
                break;
            }
            case 'w':
            {
                count_words(optarg, is_default);
                break;
            }
            case 'm':
            {
                count_chars(optarg);
                break;
            }
            default:
                break;
        }
    }

    if (!option_found && optind < argc)
    {
        for (int i = optind; i < argc; i++)
        {
            is_default = true;
            count_lines(argv[i], is_default);
            count_words(argv[i], is_default);
            count_chars(argv[i]);
        }
    }

    return EXIT_SUCCESS;
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


void count_lines(char *file_name, bool is_default)
{
    FILE *file;
    size_t total = 0;
    char c;

    file = fopen(file_name, "r");

    if (file == NULL)
    {
        perror("error opening file");
        exit(EXIT_FAILURE);
    }

    while ((c = fgetc(file)) != EOF)
    {
        if (c == '\n')
            ++total;
    }


    fclose(file);
    if (is_default)
        printf("%zu\t", total);
    else
        printf("%zu %s\n", total, file_name);

}


void count_words(char *file_name, bool is_default)
{
    FILE *file;
    size_t total = 0;
    char c;
    bool in_word;

    file = fopen(file_name, "r");

    if (file == NULL)
    {
        perror("error opening file");
        exit(EXIT_FAILURE);
    }

    while ((c = fgetc(file)) != EOF)
    {
        if (isspace(c))
        {
            in_word = false;
        }
        else if (!in_word)
        {
            in_word = true;
            ++total;
        }
    }

    fclose(file);
    if (is_default)
        printf("%zu\t", total);
    else
        printf("%zu %s\n", total, file_name);

}


void count_chars(char *file_name)
{
    FILE *file;
    size_t total = 0;
    char c;

    file = fopen(file_name, "r");

    if (file == NULL)
    {
        perror("error opening file");
        exit(EXIT_FAILURE);
    }

    while ((c = fgetc(file)) != EOF)
    {
        ++total;
    }

    fclose(file);

    printf("%zu %s\n", total, file_name);


}