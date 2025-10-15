// Lex Albrandt
// albrandt@pdx.edu
// CS333
// cae-xor source file


#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

// Command line options
// -e encrypt (argument required)
// -d decrypt (argument required)
// -h help (no argument required)
// -D diagnostic (no argument required)
// UPDATE THESE
#define OPTIONS "e: d: hD"

// Noisy debug print
#ifdef NOISY_DEBUG
# define NOISY_DEBUG_PRINT fprintf(stderr, "%s %s %d\n", __FILE__, __func__, __LINE__)
#else 
# define NOISY_DEBUG_PRINT
#endif // NOISY_DEBUG


int main(int argc, char *argv[])
{

    // getopt structure
    {
        int opt = 0;                        // getopt option variable

    }

    return EXIT_SUCCESS;
}