// Lex Albrandt
// CS 333
// Lab 3

// System includes
#include <stdlib.h>                             // Allows for system macros
#include <stdio.h>                              // Allows for input/output
#include <getopt.h>                             // Allows for getopt useage
#include <stdbool.h>                            // Allows for boolean usage
#include <unistd.h>                             // Allows for nice(), among other things
#include <crypt.h>                              // Allows for use of crypt()
#include <string.h>                             // Allows for use of memcpy/memset
#include <pthread.h>                            // Allows for use of threads

// Macros
#define BAD_OPTION 2                            // Exit value for bad command line option
#define CALLOC_FAILURE 3                        // Exit value for Calloc failure
#define FILE_READ_ERR 4                         // Exit value for file read error
#define OPTIONS "i:o:d:hvt:n"                   // Options for getopt
#define BUFFER 1000                             // Buffer size 1000
#define MAX_STRINGS 1000                        // Max number of strings
#define MAX_STRING_LEN 256                      // Max password length

#ifndef NICE_VALUE                              // Defines the nice value
# define NICE_VALUE 10
#endif // NICE_VALUE

// Prototypes
void print_help(char *progname);
void read_lines(char *filename, char ** info_array, int *count);
void password_crack_helper(void);
int get_next_row(void);


int main(int argc, char *argv[])
{
    //bool verbose = false;                     // Indicates verbose option selection
    //int num_threads = 1;                      // Default number of threads
    // char output_file;                        // File used for output results
    char *input_file = NULL;                    // File used for input
    char *dict_file = NULL;                     // File used for dictionary
    int password_count = 0;                     // Number of passwords read
    int hash_count = 0;                         // Number of hashes read
    char **passwords;                           // Array of char pointers for password strings
    char **hashes;                              // Array of pointes for hash strings

    // Initialize passwords to NULL
    // DON'T FORGET TO FREE THIS MEMORY!!!
    passwords = calloc(MAX_STRINGS, sizeof(char *));

    // check for calloc failure
    if (!passwords)
    {
        fprintf(stderr, "Memory allocation failure\n");
        exit(CALLOC_FAILURE);
    }

    // Initialize hash_entries to null
    // DON'T FORGET TO FREE THIS MEMORY!!!
    hashes = calloc(MAX_STRINGS, sizeof(char *));

    // check for calloc failure
    if (!hashes)
    {
        fprintf(stderr, "Memory allocation failure\n");
        exit(CALLOC_FAILURE);
    }



    // getopt structure
    {
        int opt = -1;

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            switch (opt)
            {
                // Input file name
                // This file is for the hashes, pair with passwords file
                // Required
                case 'i':
                {
                    input_file = optarg;
                    read_lines(input_file, passwords, &password_count);
                    break;
                }
                // Ouput file name
                // Not required
                case 'o':
                {
                    //output_file = optarg;
                    break;
                }
                // Dictionary file name
                // This refers to the passwords files
                // Required
                case 'd':
                {
                    dict_file = optarg;
                    read_lines(dict_file, hashes, &hash_count);
                    break;
                }
                // Help options
                case 'h':
                {
                    print_help(argv[0]);
                    exit(EXIT_SUCCESS);
                    break;
                }
                // Verbose option
                case 'v':
                {
                    //verbose = true;
                    break;
                }
                // Number of Threads
                // Required if -t option selected
                case 't':
                {
                    //num_threads = optarg;
                    break;
                }
                // Apply nice function
                // Not required
                // The nice() function changes the priority value for the calling
                // thread. The higher the value, the lower the priority
                // Note: NICE_VALUE = 10 in .h file
                case 'n':
                {
                    nice(NICE_VALUE);
                    break;
                }
                default:
                {
                    fprintf(stderr, "Bad command line option: %c\n", opt);
                    exit (BAD_OPTION);
                    break;
                }

            }

        }
    }

    return EXIT_SUCCESS;
}


// Print Help function
// Args: progname(char *)
// Returns: None
// Notes: goes to stderr
void print_help(char *progname)
{
    fprintf(stderr, "help text\n");
    fprintf(stderr, "\t%s ...\n", progname);
    fprintf(stderr, "\tOptions: [%s]\n", OPTIONS);
    fprintf(stderr, "\t\t-i file          hash file name (required)\n");
    fprintf(stderr, "\t\t-o file          output file name (default stdout)\n");
    fprintf(stderr, "\t\t-d file          dictionary file name (required)\n");
    fprintf(stderr, "\t\t-t #             number of threads to create (default == 1)\n");
    fprintf(stderr, "\t\t-n               renice to 10\n");
    fprintf(stderr, "\t\t-v               enable verbose mode\n");
    fprintf(stderr, "\t\t-h               helpful text\n");
}


// Read lines from the file parsed in getopt (or stdin),
// populates a char ** with pointers to each string
// Args: filename (char *), info_array(char **), count (int *)
// Returns: none
void read_lines(char *filename, char **info_array, int *count)
{
    FILE *file;
    int index = 0;
    char buffer[MAX_STRING_LEN];
    size_t len;

    file = fopen(filename, "r");
    if(!file)
    {
        perror(filename);
        exit(FILE_READ_ERR);
    }

    while (fgets(buffer, sizeof(buffer), file) && index < MAX_STRINGS)
    {
        len = strlen(buffer);
        // replaces the newline character with null terminator
        if (len > 0 && buffer[len - 1 ] == '\n')
        {
            buffer[len - 1] = '\0';
        }
        info_array[index] = strdup(buffer);
        index++;
    }
    fclose(file);
    // may not need count, but it's there if I do
    *count = index;
}


// Function to get the next row in a thread-safe way
// Args: none
// Returns: current_row (int)
int get_next_row(void)
{
    static int next_row = 0;
    static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
    int curr_row = 0;

    pthread_mutex_lock(&lock);                                      // Initiates mutex lock
    curr_row = next_row++;
    pthread_mutex_unlock(&lock);                                    // Unlocks mutex

    return curr_row;
}
