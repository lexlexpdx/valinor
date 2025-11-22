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
#include <pthread.h>                            // Allows for use of pthreads

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

// Structs
typedef struct hash_algs
{
    int DES_count;
    int NT_count;
    int MD5_count;
    int SHA_256_count;
    int SHA_512_count;
    int yescrypt_count;
    int gostyes_count;
    int bcrypt_count;
}hash_algs_t;

typedef struct thread_data
{
    char **hashes;
    char **passwords;
    hash_algs_t *hash_types;
    int hash_count;
    int password_count;
    FILE *output_fp;
}thread_data_t;

// Prototypes
void print_help(char *progname);
void read_lines(char *filename, char ** info_array, int *count);
//void password_crack_helper(char **hashes, char **passwords, hash_algs_t *hash_types, int hash_count, int password_count);
void *password_crack_helper(void *arg);
int get_next_row(int total_hashes);


int main(int argc, char *argv[])
{
    //bool verbose = false;                     // Indicates verbose option selection
    int num_threads = 1;                        // Default number of threads
    char *output_file;                          // File used for output results
    char *input_file = NULL;                    // File used for input
    char *dict_file = NULL;                     // File used for dictionary
    int password_count = 0;                     // Number of passwords read
    int hash_count = 0;                         // Number of hashes read
    char **passwords;                           // Array of char pointers for password strings
    char **hashes;                              // Array of pointes for hash strings
    pthread_t *threads = NULL;                  // Pointer array for threads
    long tid = 0;                               // Thread identifier
    hash_algs_t hash_types;                     // Struct for hash types
    thread_data_t thread_data;                  // Struct for thread data
    FILE *output_fp = stdout;                   // Output file pointer defaults to stdout

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

    // Initialize all values in struct to 0
    memset(&hash_types, 0, sizeof(hash_algs_t));


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
                    read_lines(input_file, hashes, &hash_count);
                    break;
                }
                // Ouput file name
                // Not required
                case 'o':
                {
                    output_file = optarg;
                    output_fp = fopen(output_file, "w");
                    if (!output_fp)
                    {
                        perror(output_file);
                        exit(FILE_READ_ERR);
                    }
                    break;
                }
                // Dictionary file name
                // This refers to the passwords files
                // Required
                case 'd':
                {
                    dict_file = optarg;
                    read_lines(dict_file, passwords, &password_count);
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
                    num_threads = atoi(optarg);
                    break;
                }
                // Apply nice function
                // Not required
                // The nice() function changes the priority value for the calling
                // thread. The higher the value, the lower the priority
                // Note: NICE_VALUE = 10 in .h file
                case 'n':
                {
                    // Just call once
                    // I need 
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

    // Initialize thread_data struct
    thread_data.hashes = hashes;
    thread_data.passwords = passwords;
    thread_data.hash_count = hash_count;
    thread_data.password_count = password_count;
    thread_data.hash_types = &hash_types;
    thread_data.output_fp = output_fp;

    // Initialize threads array
    // Since we don't know how many threads we need, we need to allocate
    // the memory dynamically
    threads = malloc(num_threads * sizeof(pthread_t));

    for (tid = 0; tid < num_threads; tid++)
    {
        pthread_create(&threads[tid], NULL, password_crack_helper, &thread_data);
    }
    for (tid = 0; tid < num_threads; tid++)
    {
        pthread_join(threads[tid], NULL);
    }

    for (int i = 0; i < password_count; i++)
    {
        free(passwords[i]);
    }

    for (int i = 0; i < hash_count; i++)
    {
        free(hashes[i]);
    }

    free(hashes);
    free(threads);

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
    fprintf(stderr, "\t\t-n               re-nice to 10\n");
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
int get_next_row(int total_hashes)
{
    static int next_hash = 0;                                        
    static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
    int curr_hash = 0;

    pthread_mutex_lock(&lock);                                      // Initiates mutex lock
    curr_hash = next_hash++;                                          // This is our CRITICAL RESOURCE
    pthread_mutex_unlock(&lock);                                    // Unlocks mutex

    if (curr_hash < total_hashes)
        return curr_hash;
    else
        return -1;
}


// Function for cracking passwords using crypt_rn()
// This function will also compare and see if hashes are cracked or not
// As well as extract the algorithm name for counting
// Args: hashes (char **), passwords (char **), hash_count(int), password_count (int)
// Returns: none
//void password_crack_helper(char **hashes, char **passwords, hash_algs_t *hash_types, int hash_count, int password_count)
void *password_crack_helper(void *arg)
{
    struct crypt_data crypt_info;                                           // Structure to pass to crypt_rn()
    char *alg_name = NULL;                                                  // Variable for algorithm name
    int hash_index = 0;                                                     // Variable for hash index
    char *target_hash = NULL;                                               // Variable for hash string
    char *result = NULL;                                                    // Variable for result from crypt_rn()
    char buffer[BUFFER];                                                    // Buffer for strtok
    thread_data_t *data = (thread_data_t *)arg;
    static pthread_mutex_t counter_lock = PTHREAD_MUTEX_INITIALIZER;        // Mutex lock
    bool cracked = false;                                                   // Variable to indicate if cracked or not

    // Initialize the crypt_data structure
    // Sets everything to 0
    memset(&crypt_info, 0, sizeof(crypt_info));

    // For loop to loop through each array of passwords and hashes
    // We want to extract the alg name for each line that is being read
    for (hash_index = get_next_row(data->hash_count); hash_index != -1 ; hash_index = get_next_row(data->hash_count))
    {
        cracked = false;
        target_hash = data->hashes[hash_index];
        
        // this section parses the algorithm name from the hash
        if (data->hashes[hash_index][0] == '$')
        {
            strncpy(buffer, data->hashes[hash_index], sizeof(buffer) - 1); // Copies hash string into buffer for parsing
            buffer[sizeof(buffer) - 1] = '\0'; // Ensure null-termination

            strtok(buffer, "$");                            // Skips the first $, first pass is the string
            alg_name = strtok(NULL, "$");                   // Parses the algorithm
        }
        else
        {
            alg_name = "DES";
        }

        // this section increments the total number of each hash algorithm based on parsed info
        // Protect with mutex lock!
        pthread_mutex_lock(&counter_lock);
        if (strcmp(alg_name, "3") == 0)

        {
            data->hash_types->NT_count++;
        }
        else if (strcmp(alg_name, "1") == 0)
        {
            data->hash_types->MD5_count++;
        }
        else if (strcmp(alg_name, "5") == 0)
        {
            data->hash_types->SHA_256_count++;
        }
        else if (strcmp(alg_name, "6") == 0)
        {
            data->hash_types->SHA_512_count++;
        }
        else if (strcmp(alg_name, "y") == 0)
        {
            data->hash_types->yescrypt_count++;
        }
        else if (strcmp(alg_name, "gy") == 0)
        {
            data->hash_types->gostyes_count++;
        }
        else if (strcmp(alg_name, "2b") == 0)
        {
            data->hash_types->bcrypt_count++;
        }
        else if (strcmp(alg_name, "DES") == 0)
        {
            data->hash_types->DES_count++;
        }
        // Unlock the mutex lock!
        pthread_mutex_unlock(&counter_lock);

        // check each password against the hash
        for (int p = 0; p < data->password_count; p++)
        {
            result = crypt_rn(data->passwords[p], target_hash, &crypt_info, sizeof(crypt_info));
            if (result && (strcmp(result, target_hash) == 0))
            {
                fprintf(data->output_fp, "cracked  %s  %s\n", data->passwords[p], target_hash);
                cracked = true;
                // break if password cracked
                break;
            }
        }
        if (!cracked)
            fprintf(data->output_fp, "*** failed to crack  %s\n", target_hash);

    }
    return NULL;
}

