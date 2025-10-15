// Lex Albrandt
// albrandt@pdx.edu
// CS333
// cae-xor source file


#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <getopt.h>

// Command line options
// -e encrypt (argument required)
// -d decrypt (argument required)
// -c encryption for caesar only (argument required)
// -x encryption for xor only (argument required)
// -h help (no argument required)
// -D diagnostic (no argument required)
// UPDATE THESE
#define OPTIONS "e: d: c: x: hD"

// Noisy debug print
// -DNOISY_DEBUG in makefile (disable there)
#ifdef NOISY_DEBUG
# define NOISY_DEBUG_PRINT fprintf(stderr, "%s %s %d\n", __FILE__, __func__, __LINE__)
#else 
# define NOISY_DEBUG_PRINT
#endif // NOISY_DEBUG


int main(int argc, char *argv[])
{
    NOISY_DEBUG_PRINT;
    // getopt structure
    {
        int opt = 0;                        // getopt option variable

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            switch(opt)
            {
                // encrypt (argument required)
                case 'e':
                    NOISY_DEBUG_PRINT;
                    printf("encrypt string: %s\n", optarg);
                    break;
                // decrypt (argument required) 
                case 'd':
                    NOISY_DEBUG_PRINT;
                    printf("decrypt string: %s\n", optarg);
                    break;
                // encrypt with caesar cipher only (argument required)
                case 'c':
                    NOISY_DEBUG_PRINT;
                    printf("encrypt string: %s\n", optarg);
                    break;
                // encrypt with xor cipher only (argument required)
                case 'x':
                    NOISY_DEBUG_PRINT;
                    printf("encrypt string: %s\n", optarg);
                    break;
                // help (no argument required)
                // UPDATE LATER
                case 'h':
                    NOISY_DEBUG_PRINT;
                    printf("helpful info\n");
                    break;
                // Diagnostic info
                // UPDATE LATER
                case 'D':
                    NOISY_DEBUG_PRINT;
                    printf("Diagnostic info\n");
                    break;
                default:
                    NOISY_DEBUG_PRINT;
                    break;
            }
        }
        NOISY_DEBUG_PRINT;

    }

    return EXIT_SUCCESS;
}