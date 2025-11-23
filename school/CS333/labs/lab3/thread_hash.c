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
#include <sys/time.h>                           // Allows for finding times

// Macros
#define BAD_OPTION 2                            // Exit value for bad command line option
#define CALLOC_FAILURE 3                        // Exit value for Calloc failure
#define FILE_READ_ERR 4                         // Exit value for file read error
#define OPTIONS "i:o:d:hvt:n"                   // Options for getopt
#define BUFFER 1000                             // Buffer size 1000
#define MAX_STRINGS 1000                        // Max number of strings
#define MAX_STRING_LEN 256                      // Max password length
#define MICROSECONDS_PER_SECOND 1000000.0       // Microseconds per second


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
    int failed;
    int total;
    int thread_time;
}hash_algs_t;

typedef struct thread_data
{
    char **hashes;
    char **passwords;
    hash_algs_t *hash_types;
    int hash_count;
    int password_count;
    FILE *output_fp;
    long tid;
    int total_failed;
    struct timeval et1;
    struct timeval et2;
}thread_data_t;

// Prototypes
void print_help(char *progname);
void read_lines(char *filename, char ** info_array, int *count);
void *password_crack_helper(void *arg);
int get_next_row(int total_hashes);
double elapsed_time(struct timeval *t1, struct timeval *t2);


int main(int argc, char *argv[])
{
    //bool verbose = false;                     // Indicates verbose option selection
    int num_threads = 1;                        // Default number of threads
    char *output_file = NULL;                   // File used for output results
    char *input_file = NULL;                    // File used for input
    char *dict_file = NULL;                     // File used for dictionary
    int password_count = 0;                     // Number of passwords read
    int hash_count = 0;                         // Number of hashes read
    char **passwords;                           // Array of char pointers for password strings
    char **hashes;                              // Array of pointes for hash strings
    pthread_t *threads = NULL;                  // Pointer array for threads
    long tid = 0;                               // Thread identifier
    hash_algs_t hash_types;                     // Struct for hash types
    thread_data_t *thread_data_array;           // Array of thread data structs
    FILE *output_fp = stdout;                   // Output file pointer defaults to stdout
    int total_failed = 0;                       // Counts total failed cracks
    struct timeval et0;                         // Start time for all threads
    struct timeval et3;                         // End time for all threads
    double total_time = 0.0;                    // Total time for all threads


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

    // Sets et0 to current time
    gettimeofday(&et0, NULL);

    // Initialize threads array
    // Since we don't know how many threads we need, we need to allocate
    // the memory dynamically
    threads = malloc(num_threads * sizeof(pthread_t));

    // Initialize thread data struct array
    thread_data_array = malloc(num_threads * sizeof(thread_data_t));

    // Create threads
    for (tid = 0; tid < num_threads; tid++)
    {
        // Initialize thread_data struct
        thread_data_array[tid].hashes = hashes;
        thread_data_array[tid].passwords = passwords;
        thread_data_array[tid].hash_count = hash_count;
        thread_data_array[tid].password_count = password_count;
        thread_data_array[tid].hash_types = &hash_types;
        thread_data_array[tid].output_fp = output_fp;
        thread_data_array[tid].tid = tid;
        thread_data_array[tid].total_failed = total_failed;
    
        pthread_create(&threads[tid], NULL, password_crack_helper, &thread_data_array[tid]);
    }
    for (tid = 0; tid < num_threads; tid++)
    {
        pthread_join(threads[tid], NULL);
    }

    // Set time of day for all threads finishing
    gettimeofday(&et3, NULL);

    // Calculate total time for all threads
    total_time = elapsed_time(&et0, &et3);
    

    // Print out totals
    fprintf(stderr, "total:  %2d", num_threads);
    fprintf(stderr, "     %.2lf sec", total_time);
    fprintf(stderr, "               DES: %5d", hash_types.DES_count);
    fprintf(stderr, "                NT: %5d", hash_types.NT_count);
    fprintf(stderr, "               MD5: %5d", hash_types.MD5_count);
    fprintf(stderr, "            SHA256: %5d", hash_types.SHA_256_count);
    fprintf(stderr, "            SHA512: %5d", hash_types.SHA_512_count);
    fprintf(stderr, "          YESCRYPT: %5d", hash_types.yescrypt_count);
    fprintf(stderr, "     GOST_YESCRYPT: %5d", hash_types.gostyes_count);
    fprintf(stderr, "            BCRYPT: %5d", hash_types.bcrypt_count);
    fprintf(stderr, "  total: %9d", hash_count);
    fprintf(stderr, "  failed: %9d\n", hash_types.failed);


    // Free memory
    for (int i = 0; i < password_count; i++)
    {
        free(passwords[i]);
    }

    for (int i = 0; i < hash_count; i++)
    {
        free(hashes[i]);
    }

    free(passwords);
    free(hashes);
    free(threads);
    free(thread_data_array);

    if (output_fp != stdout)
    {
        fclose(output_fp);
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

    *count = index;
}


// Function to get the next row in a thread-safe way
// Args: total_hashes (int)
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
    thread_data_t *data = (thread_data_t *)arg;                             // All thread data
    static pthread_mutex_t counter_lock = PTHREAD_MUTEX_INITIALIZER;        // Mutex lock
    bool cracked = false;                                                   // Variable to indicate if cracked or not
    hash_algs_t local_counts;                                               // Variable for local thread counts
    double thread_time = 0.0;                                               // Variable for thread time

    // Sets time for starting of single thread
    gettimeofday(&data->et1, NULL);

    // Initialize the crypt_data structure
    // Sets everything to 0
    memset(&crypt_info, 0, sizeof(crypt_info));

    // Initialize local counts
    memset(&local_counts, 0, sizeof(local_counts));

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

            alg_name = strtok(buffer, "$");                            // Skips the first $, and returns the pointer to the next delimeter
        }
        else
        {
            alg_name = "DES";
        }

        // this section increments the number of algorithms for each thread
        if (strcmp(alg_name, "3") == 0)
        {
            local_counts.NT_count++;
        }
        else if (strcmp(alg_name, "1") == 0)
        {
            local_counts.MD5_count++;
        }
        else if (strcmp(alg_name, "5") == 0)
        {
            local_counts.SHA_256_count++;
        }
        else if (strcmp(alg_name, "6") == 0)
        {
            local_counts.SHA_512_count++;
        }
        else if (strcmp(alg_name, "y") == 0)
        {
            local_counts.yescrypt_count++;
        }
        else if (strcmp(alg_name, "gy") == 0)
        {
            local_counts.gostyes_count++;
        }
        else if (strcmp(alg_name, "2b") == 0)
        {
            local_counts.bcrypt_count++;
        }
        else if (strcmp(alg_name, "DES") == 0)
        {
            local_counts.DES_count++;
        }

        // check each password against the hash
        for (int p = 0; p < data->password_count; p++)
        {
            result = crypt_rn(data->passwords[p], target_hash, &crypt_info, sizeof(crypt_info));
            if (result && (strcmp(result, target_hash) == 0))
            {
                fprintf(data->output_fp, "cracked  %s  %s\n", data->passwords[p], target_hash);
                cracked = true;
                local_counts.total++;
                // break if password cracked
                break;
            }
        }
        if (!cracked)
        {
            fprintf(data->output_fp, "*** failed to crack  %s\n", target_hash);
            local_counts.failed++;
            local_counts.total++;
        }
    }

    // Update the global counts
    // Protect with a mutex lock!
    pthread_mutex_lock(&counter_lock);
    data->hash_types->NT_count += local_counts.NT_count;
    data->hash_types->MD5_count += local_counts.MD5_count;
    data->hash_types->SHA_256_count += local_counts.SHA_256_count;
    data->hash_types->SHA_512_count += local_counts.SHA_512_count;
    data->hash_types->yescrypt_count += local_counts.yescrypt_count;
    data->hash_types->gostyes_count += local_counts.gostyes_count;
    data->hash_types->bcrypt_count += local_counts.bcrypt_count;
    data->hash_types->DES_count += local_counts.DES_count;
    data->hash_types->failed += local_counts.failed;
    pthread_mutex_unlock(&counter_lock);

    // Set time for end of thread process
    gettimeofday(&data->et2, NULL);

    // Get total time for this thread
    thread_time = elapsed_time(&data->et1, &data->et2);

    // Print out results
    fprintf(stderr, "thread:  %ld", data->tid);
    fprintf(stderr, "     %.2lf sec", thread_time);
    fprintf(stderr, "               DES: %5d", local_counts.DES_count);
    fprintf(stderr, "                NT: %5d", local_counts.NT_count);
    fprintf(stderr, "               MD5: %5d", local_counts.MD5_count);
    fprintf(stderr, "            SHA256: %5d", local_counts.SHA_256_count);
    fprintf(stderr, "            SHA512: %5d", local_counts.SHA_512_count);
    fprintf(stderr, "          YESCRYPT: %5d", local_counts.yescrypt_count);
    fprintf(stderr, "     GOST_YESCRYPT: %5d", local_counts.gostyes_count);
    fprintf(stderr, "            BCRYPT: %5d", local_counts.bcrypt_count);
    fprintf(stderr, "  total: %9d", local_counts.total);
    fprintf(stderr, "  failed: %9d\n", local_counts.failed);

    pthread_exit(EXIT_SUCCESS);
}


// Elapsed time from start to finish
// Args: t0(start time) (timeval *), t1(end time) (timeval *)
// Returns: elapsed time (double)
double elapsed_time(struct timeval *t0, struct timeval *t1)
{
    double elapsed_time = 0;

    elapsed_time = (((double) (t1->tv_sec - t0->tv_sec)))
                + ((double) (t1->tv_usec - t0->tv_usec)) / MICROSECONDS_PER_SECOND;

    return elapsed_time;
}