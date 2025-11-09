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
#define BUFFER_SIZE 1000
#define DIGEST_SIZE 16
#define HEX_DIGEST_SIZE 33
#define HEX_DIGIT_BUFF 3

// Prototypes
void print_help(char *progname);
void create_archive(char *archive_name, int argc, char *argv[], int optind);
void table_of_contents(char *archive_name, bool is_verbose);

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
        create_archive(archive_name, argc, argv, optind);
    }

    else if (mode_flag == EXTRACT)
        printf("Do extract thing\n");
    else if (mode_flag == VALIDATE)
        printf("Do validate thing\n");
    else if (mode_flag == TABLE)
    {
        table_of_contents(archive_name, verbose);
    }


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


void create_archive(char *archive_name, int argc, char *argv[], int optind)
{
    size_t name_len = 0;
    size_t position = 0;
    int archive_fd = -1;
    int file_fd = -1;
    char *file_name = NULL;
    mode_t new_mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH;          // rw-rw-r permissions
    arvik_header_t new_header;
    arvik_footer_t new_footer;
    struct stat sb;
    ssize_t bytes_written;
    ssize_t bytes_read;
    unsigned char buffer[BUFFER_SIZE];
    char temp[ARVIK_NAME_LEN + 1];
    char header_buf[ARVIK_NAME_LEN +
                    ARVIK_DATE_LEN +
                    ARVIK_UID_LEN +
                    ARVIK_GID_LEN +
                    ARVIK_MODE_LEN +
                    ARVIK_SIZE_LEN +
                    ARVIK_TERM_LEN];
    unsigned char md4_header_digest[DIGEST_SIZE];
    unsigned char md4_data_digest[DIGEST_SIZE];
    char md4_header_hex[HEX_DIGEST_SIZE];
    char md4_data_hex[HEX_DIGEST_SIZE];
    MD4_CTX md4_ctx;

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
        if (file_fd < 0)
        {
            perror(file_name);
            continue;
        }
        position = 0;

        // fill arvik header_t
        fstat(file_fd, &sb);
        
        // File Name (as string)
        // important to set the character after the end of the file name with '<'
        name_len = strlen(file_name);
        memset(new_header.arvik_name, ' ', ARVIK_NAME_LEN);
        memcpy(new_header.arvik_name, file_name, name_len);
        if (name_len >= ARVIK_NAME_LEN)
            name_len = ARVIK_NAME_LEN - 1;
        new_header.arvik_name[name_len] = '<';


        // In this section we use snprintf to give the max number of bytes
        // to write instead of sprintf, which can overflow the buffer
        // memcpy copies blindly, so it will copy exactly what you want, including
        // null terminators
        // We want inject the data into the struct first (with snprintf), then
        // copy that data to a temp array without worrying about the null terminators
        // We use memcpy for writing to the header and footer allowing us to place
        // the strings exactly where we want them so the byte positions are preserved

        // Date (mt as a decimal string) 
        snprintf(temp, sizeof(temp), "%-14ld", sb.st_mtime);
        memcpy(new_header.arvik_date, temp, ARVIK_DATE_LEN);

        // UID (as decimal)
        snprintf(temp, sizeof(temp), "%-6d", sb.st_uid);
        memcpy(new_header.arvik_uid, temp, ARVIK_UID_LEN);

        // GID (as decimal string)
        snprintf(temp, sizeof(temp), "%-6d", sb.st_gid);
        memcpy(new_header.arvik_gid, temp, ARVIK_GID_LEN);

        // Mode (as octal string)
        snprintf(temp, sizeof(temp), "%-8o", sb.st_mode);
        memcpy(new_header.arvik_mode, temp, ARVIK_MODE_LEN);

        // Size (as decimal string)
        snprintf(temp, sizeof(temp), "%-12ld", sb.st_size);
        memcpy(new_header.arvik_size, temp, ARVIK_SIZE_LEN);

        // Arvik term
        memcpy(new_header.arvik_term, ARVIK_TERM, ARVIK_TERM_LEN);

        // fill header buffer to write to archive
        // Here we are concatenating all of the header info together into one long
        // string that is of fixed width, again using memcpy to ignore null terminators
        memcpy(header_buf + position, new_header.arvik_name, ARVIK_NAME_LEN);
        position += ARVIK_NAME_LEN;
        memcpy(header_buf + position, new_header.arvik_date, ARVIK_DATE_LEN);
        position += ARVIK_DATE_LEN;
        memcpy(header_buf + position, new_header.arvik_uid, ARVIK_UID_LEN);
        position += ARVIK_UID_LEN;
        memcpy(header_buf + position, new_header.arvik_gid, ARVIK_GID_LEN);
        position += ARVIK_GID_LEN;
        memcpy(header_buf + position, new_header.arvik_mode, ARVIK_MODE_LEN);
        position += ARVIK_MODE_LEN;
        memcpy(header_buf + position, new_header.arvik_size, ARVIK_SIZE_LEN);
        position += ARVIK_SIZE_LEN;
        memcpy(header_buf + position, new_header.arvik_term, ARVIK_TERM_LEN);
        position += ARVIK_TERM_LEN;


        // MD4 header
        MD4Init(&md4_ctx);
        MD4Update(&md4_ctx, (uint8_t *)header_buf, sizeof(header_buf));
        MD4Final(md4_header_digest, &md4_ctx);

        // Here we are converting the raw header data into a two-digit hex string
        for (int j = 0; j < DIGEST_SIZE; j++)
        {
            snprintf(md4_header_hex + 2 * j, HEX_DIGIT_BUFF, "%02x", md4_header_digest[j]);
        }

        // Write the header to the archive
        write(archive_fd, header_buf, sizeof(header_buf));

        // MD4 data
        // Here we initialize a new MD4 for the data portion of the file
        // we must lseek back to the beginning of the file, and read again, as before
        // We update the MD4 inside the loop as we go, then finalize
        MD4Init(&md4_ctx);
        lseek(file_fd, 0, SEEK_SET);
        while ((bytes_read = read(file_fd, buffer, BUFFER_SIZE)) > 0)
        {
            bytes_written = write(archive_fd, buffer, bytes_read);
            if (bytes_written != bytes_read)
            {
                perror("write to archive");
                exit(EXIT_FAILURE);
            }

            MD4Update(&md4_ctx, buffer, bytes_read);
        }

        MD4Final(md4_data_digest, &md4_ctx);

        // convert data MD4 to hex as with header data
        for (int j = 0; j < DIGEST_SIZE; j++)
        {
            snprintf(md4_data_hex + 2 * j, HEX_DIGIT_BUFF, "%02x", md4_data_digest[j]);
        }

        // copies 32-char hex string for the md4 data to the footer
        memcpy(new_footer.md4sum_data, md4_data_hex, 32);

        // copies arvik term to footer
        memcpy(new_footer.arvik_term, ARVIK_TERM, ARVIK_TERM_LEN);

        // write header MD4 to archive
        write(archive_fd, md4_header_hex, 32);

        // write footer data to archive
        write(archive_fd, new_footer.md4sum_data, 32);

        // write arvik term to archive
        write(archive_fd, new_footer.arvik_term, ARVIK_TERM_LEN);

        close(file_fd);
    }

    if (archive_fd != STDOUT_FILENO)
        close(archive_fd);

}


void table_of_contents(char *file_name, bool is_verbose)
{
    off_t file_skip;
    int iarch = STDIN_FILENO;
    char buffer[BUFFER_SIZE];
    arvik_header_t metadata;
    arvik_footer_t metadata_foot;
    char *back_pos = NULL;
    char size_buffer[ARVIK_SIZE_LEN + 2] = {0};

    if (file_name != NULL)
    {
        iarch = open(file_name, O_RDONLY);
    }

    read(iarch, buffer, strlen(ARVIK_TAG));

    if (strncmp(buffer, ARVIK_TAG, strlen(ARVIK_TAG)) != 0)
    {
        fprintf(stderr, "Invalid arvik file\n");
        exit(EXIT_FAILURE);
    }

    while(read(iarch, &metadata, sizeof(arvik_header_t)) > 0)
    {
        memset(buffer, 0, BUFFER_SIZE);
        strncpy(buffer, metadata.arvik_name, ARVIK_NAME_LEN);
        if ((back_pos = strchr(buffer, ARVIK_NAME_TERM)))
        {
            *back_pos = '\0';
        }
        printf("%s\n", buffer);

        memset(size_buffer, 0, sizeof(size_buffer));
        memcpy(size_buffer, metadata.arvik_size, ARVIK_SIZE_LEN);
        file_skip = atoi(size_buffer);
        if (file_skip % 2 != 0)
            file_skip += 1;
        lseek(iarch, file_skip, SEEK_CUR);
        read(iarch, &metadata_foot, sizeof(arvik_footer_t));
    }

    if (file_name != NULL)
    {
        close(iarch);
    }

    if (is_verbose)
        printf("It's verbose");
}