// Lex Albrandt
// CS333
// Lab2

// System includes
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <md4.h>
#include <getopt.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

// Local includes
#include "arvik.h"

// Macros
#define CREATE 1
#define VALIDATE 2
#define TABLE 3
#define EXTRACT 4

// Prototypes
void print_help(char *progname);
void create_archive(char *archive_name, bool is_verbose, int argc, char *argv[], int optind);

int main(int argc, char *argv[])
{
    int mode_flag = -1;
    char *archive_name = NULL;
    bool verbose = false;

    // getopt structure
    {
        int opt = 0;

        while ((opt = getopt(argc, argv, ARVIK_OPTIONS)) != -1)
        {
            switch(opt)
            {
                // create
                case 'c':
                    mode_flag = CREATE;
                    break;
                // extract
                case 'x':
                    mode_flag = EXTRACT;
                    break;
                // table of contents
                case 't':
                    mode_flag = TABLE;
                    break;
                // file name
                case 'f':
                    archive_name = optarg;
                    break;
                // help
                case 'h':
                    print_help(argv[0]);
                    break;
                // verbose
                case 'v':
                    // this will be in file print function
                    // gives mode, uid, gid, size, mtime, header md4, data md4
                    verbose = true;
                    break;
                // validate
                case 'V':
                    mode_flag = VALIDATE;
                    break;
            }
        }
    }

    if (mode_flag == CREATE)
    {
        create_archive(archive_name, verbose, argc, argv, optind);
    }

    else if (mode_flag == EXTRACT)
        printf("Do extract thing\n");
    else if (mode_flag == VALIDATE)
        printf("Do validate thing\n");
    else if (mode_flag == TABLE)
        printf("Do table of contents thing\n");


    return EXIT_SUCCESS;
}


void print_help(char *progname)
{
    printf("Usage: %s -[%s] archive_file file...\n", progname, ARVIK_OPTIONS);
    printf("        -c           create new archive file\n");
    printf("        -x           extract members from an existing archive file\n");
    printf("        -t           show the table of contents of the archive file\n");
    printf("        -f filename  name of the archive file to use\n");
    printf("        -V           Validate the md4 values from the header and data\n");
    printf("        -v           verbose output\n");
    printf("        -h           show help text\n");
}


void create_archive(char *archive_name, bool is_verbose, int argc, char *argv[], int optind)
{
    int archive_fd = -1;
    int file_fd = -1;
    char *file_name = NULL;
    mode_t new_mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH;          // rw-rw-r permissions
    arvik_header_t new_header;
    struct stat sb;

    // Open archive file
    if (archive_name)
        archive_fd = open(archive_name, O_WRONLY | O_CREAT | O_TRUNC, new_mode);
    else
        archive_fd = STDOUT_FILENO;
    
    // file descriptor error check
    if (archive_fd < 0)
    {
        perror("open archive");
        exit(EXIT_FAILURE);
    }

    // write arvik tag at beginning of every new arvik archive file
    write(archive_fd, ARVIK_TAG, strlen(ARVIK_TAG));

    // loop through command line files 
    for (int i = optind; i < argc; i++)
    {
        file_name = argv[i];
        file_fd = open(file_name, O_RDONLY);

        // fill arvik header_t
        fstat(file_fd, &sb);                            // fills the sb struct with metadata
        
        // File Name (as string)
        strncpy(new_header.arvik_name, file_name, ARVIK_NAME_LEN -1);
        new_header.arvik_name[ARVIK_NAME_LEN -1] = ARVIK_NAME_TERM;

        // Date (mt as a decimal string) 
        snprintf(new_header.arvik_date, ARVIK_DATE_LEN, "%ld", sb.st_mtime);

        // UID (as decimal)
        snprintf(new_header.arvik_uid, ARVIK_UID_LEN, "%d", sb.st_uid);

        // GID (as decimal string)
        snprintf(new_header.arvik_gid, ARVIK_GID_LEN, "%d", sb.st_gid);

        // Mode (as octal string)
        snprintf(new_header.arvik_mode, ARVIK_MODE_LEN, "%o", sb.st_mode);

        // Size (as decimal string)
        snprintf(new_header.arvik_size, ARVIK_SIZE_LEN, "%ld", sb.st_size);

        // Arvik term
        strncpy(new_header.arvik_term, ARVIK_TERM, ARVIK_TERM_LEN - 1);
        new_header.arvik_term[ARVIK_TERM_LEN -1] = '\0';

    }

    if (is_verbose)
        printf("it's verbose");


}