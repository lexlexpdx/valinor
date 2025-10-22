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
#include <pwd.h>
#include <grp.h>

#define _GNU_SOURCE
#define BUFFER 200

// Prototypes
void print_mode(mode_t mode);
void print_time(time_t time);

int main(int argc, char *argv[])
{
    struct stat sb;
    struct passwd *pw;
    struct group *grp;

    // Checks to ensure user added file path to CLI
    // If there are not exactly two arguments, failure will occur
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <pathname>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Populates the stat structure 'sb' with information about the file
    // If this fails a -1 is returned
    if (lstat(argv[1], &sb) == -1)
    {
        perror("lstat failure");
        exit(EXIT_FAILURE);
    }

    // Print file path
    printf("File: %s\n", argv[1]);

    // Print device ID number (will be different on different machines)
    printf("%-27s %ju\n", "  Device ID number: ", (uintmax_t)sb.st_dev);

    // Print file type
    printf("%-27s", "  File type:");
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
            printf(" regular file\n");
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
    
    // Print inode information
    printf("%-27s %ju\n", "  I-node number:", (uintmax_t) sb.st_ino);

    // Print human-readable mode information
    print_mode(sb.st_mode);

    // Print link count information 
    printf("%-27s %ju\n", "  Link count:", (uintmax_t) sb.st_nlink);

    // Print owner information
    pw = getpwuid(sb.st_uid);
    printf("%-27s %s\t\t(UID = %ju)\n", "  Owner Id:", pw->pw_name, (uintmax_t)sb.st_uid);

    // Print group id information
    grp = getgrgid(sb.st_gid);
    printf("%-27s %s\t\t(GID = %ju)\n", "  Group Id:", grp->gr_name, (uintmax_t)sb.st_gid);

    // Print Preferred I/O block size
    printf("%-27s %jd bytes\n", "  Preferred I/O block size:", (intmax_t) sb.st_blksize);

    // Print file size
    printf("%-27s %jd bytes\n", "  File size:", (intmax_t)sb.st_size);

    // Print Blocks allocated
    printf("%-27s %jd\n", "  Blocks allocated:", (intmax_t)sb.st_blocks);

    // Print LFA epoch
    printf("%-27s %jd (seconds since the epoch)\n", "  Last file access:", (intmax_t)sb.st_atime);

    // Print LFM epoch
    printf("%-27s %jd (seconds since the epoch)\n", "  Last file modification:", (intmax_t)sb.st_mtime);

    // Print LSC epoch
    printf("%-27s %jd (seconds since the epoch)\n", "  Last status change:", (intmax_t)sb.st_ctime);

    // Print LFA local
    print_time(sb.st_atime);

    // Print LFM local
    print_time(sb.st_mtime);

    // Print LSC local
    print_time(sb.st_ctime);



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
    printf("%-27s %c%s\t\t(%03o in octal)\n",
            "  Mode:", type, perms, octal);

}


void print_time(time_t time)
{
    struct tm *local_time;
    char buffer[BUFFER];

    
    local_time = localtime(&time);

    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S %z (%Z) %a (local)\n", local_time);

    printf("%-27s %s", "  Last file access:", buffer);
}