// Lex Albrandt
// CS333
// Lab 1
// mystat source code

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/sysmacros.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define _GNU_SOURCE

// Prototypes
void print_mode(mode_t mode);

int main(int argc, char *argv[])
{
    struct stat sb;

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <pathname>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if (lstat(argv[1], &sb) == -1)
    {
        perror("lstat");
        exit(EXIT_FAILURE);
    }
    printf("File: %s\n", argv[1]);
    printf("%-30s %ju\n", "  Device ID number: ", (uintmax_t)sb.st_dev);
    printf("%-31s", "  File type: ");
    switch (sb.st_mode & S_IFMT)
    {
        case S_IFBLK:
        {
            printf("block device\n");
            break;
        }
        case S_IFCHR:
        {
            printf("character device\n");
            break;
        }
        case S_IFDIR:
        {
            printf("directory\n");
            break;
        }
        case S_IFIFO:
        {
            printf("FIFO/pipe\n");
            break;
        }
        case S_IFLNK:
        {
            printf("Symbolic link - with dangling destination\n");
            break;
        }
        case S_IFREG:
        {
            printf("regular file\n");
            break;
        }
        case S_IFSOCK:
        {
            printf("socket\n");
            break;
        }
        default:
        {
            printf("unknown?\n");
            break;
        }
    }
    printf("%-30s %ju\n", "  I-node number:", (uintmax_t) sb.st_ino);
    //printf("%-30s %jo\n", "  Mode:", (uintmax_t) sb.st_mode);
    print_mode(sb.st_mode);

    return EXIT_SUCCESS;
}


void print_mode(mode_t mode)
{
    char type;
    char perms[10];
    unsigned int octal;

    // File type
    if (S_ISREG(mode))
        type = '-';
    else if (S_ISDIR(mode))
        type = 'd';
    else if (S_ISCHR(mode)) 
        type = 'c';
    else if (S_ISBLK(mode))
        type = 'b';
    else if (S_ISFIFO(mode))
        type = 'p';
    else if (S_ISLNK(mode))
        type = 'l';
    else if (S_ISSOCK(mode))
        type = 's';

    // File Permissions
    // User perms
    perms[0] = (mode & S_IRUSR) ? 'r' : '-';
    perms[1] = (mode & S_IWUSR) ? 'w' : '-';
    perms[2] = (mode & S_IXUSR) ? 'x' : '-';

    // Group perms
    perms[3] = (mode & S_IRGRP) ? 'r' : '-';
    perms[4] = (mode & S_IWGRP) ? 'w' : '-';
    perms[5] = (mode & S_IXGRP) ? 'x' : '-';

    // Other perms
    perms[6] = (mode & S_IROTH) ? 'r' : '-';
    perms[7] = (mode & S_IWOTH) ? 'w' : '-';
    perms[8] = (mode & S_IXOTH) ? 'x' : '-';

    // Null-terminate
    perms[9] = '\0';
    
    // Octal printout (lower 3 bytes of mode)
    octal = mode & 0777;

    // Formatting
    printf("%-30s %c%s          (%03o in octal)\n",
            "  Mode:", type, perms, octal);

}