// Lex Albrandt
// CS 333
// Lab 3

// System includes
#include <stdlib.h>                         // Allows for system macros
#include <stdio.h>                          // Allows for input/output
#include <getopt.h>                         // Allows for getopt useage
#include <stdbool.h>                        // Allows for boolean usage
#include <unistd.h>                         // Allows for nice(), among other things

// Local includes
#include "thread_hash.h"                    // Local supplied .h file

// Macros
#define BAD_OPTION 2                        // Exit value for bad command line option

// Prototypes
void print_help(char *progname);

int main(int argc, char *argv[])
{
    //bool verbose = false;                     // Indicates verbose option selection
    //int num_threads = 1;                      // Default number of threads
    // char output_file;                        // File used for output results
    // char input_file;                         // File used for input
    // char dict_file;                          // File used for dictionary

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
                    // input_file = optarg;
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
                    //dict_file = optarg;
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
        // THIS IS JUST TO COMPILE UNTIL IT IS USED
        // REMOVE WHEN DONE!!!!!!!!!
        if (false)
        {
            printf("%s\n", *algorithm_string);
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
    fprintf(stderr, "\t\t-d file          dictionary file name (default stdout)\n");
    fprintf(stderr, "\t\t-t #             number of threads to create (default 1)\n");
    fprintf(stderr, "\t\t-n               renice to 10\n");
    fprintf(stderr, "\t\t-v               enable verbose mode\n");
    fprintf(stderr, "\t\t-h               helpful text\n");
}