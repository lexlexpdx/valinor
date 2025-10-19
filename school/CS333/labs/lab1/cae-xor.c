// Lex Albrandt
// albrandt@pdx.edu
// CS333
// cae-xor source file


#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>

// Command line options
// -e encrypt (argument required)
// -d decrypt (argument required)
// -c encryption for caesar only (argument required)
// -x encryption for xor only (argument required)
// -h help (no argument required)
// -D diagnostic (no argument required)
#define OPTIONS "e:d:c:x:hD"
#define BUFFER_SIZE 5000
#define PRINT_CHAR_START 32
#define PRINT_CHAR_END 126
#define PRINT_RANGE (PRINT_CHAR_END - PRINT_CHAR_START + 1)

// Noisy debug print
// -DNOISY_DEBUG in makefile (disable there)
#ifdef NOISY_DEBUG
# define NOISY_DEBUG_PRINT fprintf(stderr, "%s %s %d\n", __FILE__, __func__, __LINE__)
#else 
# define NOISY_DEBUG_PRINT
#endif // NOISY_DEBUG

// Prototypes
void caesar_encrypt(char *);

int main(int argc, char *argv[])
{
    bool enc_dec = false;               // if enc_dec == true: encrypt was last to be seen, else decrypt was last to be seen
    char *key_string = NULL;           // stores optarg for processing after command line is parsed

    NOISY_DEBUG_PRINT;

    // getopt structure
    {
        int opt = 0;                        // getopt option variable

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            NOISY_DEBUG_PRINT;
            switch(opt)
            {
                // encrypt (argument required)
                case 'e':
                    enc_dec = true;
                    key_string = optarg;
                    break;
                // decrypt (argument required) 
                case 'd':
                    enc_dec = false;
                    key_string = optarg;
                    break;
                // encrypt with caesar cipher only (argument required)
                case 'c':
                    key_string = optarg;
                    caesar_encrypt(key_string);
                    break;
                // encrypt with xor cipher only (argument required)
                case 'x':
                    key_string = optarg;
                    break;
                // help (no argument required)
                // UPDATE LATER
                case 'h':
                    printf("helpful info\n");
                    break;
                // Diagnostic info
                // UPDATE LATER
                case 'D':
                    printf("Diagnostic info\n");
                    break;
                default:
                    break;
            }
        }
        NOISY_DEBUG_PRINT;
        if (enc_dec)
        {
            // pass to encryption function
            printf("Encryption function will be called on %s\n", key_string);
            caesar_encrypt(key_string);
        }
        else
        {
            // pass to decryption function
            printf("Decryption function will be called on %s\n", key_string);
        }
    }


    return EXIT_SUCCESS;
}

void caesar_encrypt(char *key_string)
{
    char character;
    char buffer[BUFFER_SIZE];
    ssize_t num_bytes_read = 0;
    size_t key_length = strlen(key_string);
    size_t key_index;
    int shift = 0;

    NOISY_DEBUG_PRINT;
    while ((num_bytes_read = read(0, buffer, BUFFER_SIZE)) > 0)
    {
        for (ssize_t i = 0; i < num_bytes_read; i++)
        {
            character = buffer[i];
            if (isprint(character))                                                                         // only runs if the character is printable
            {
                shift = key_string[key_index % key_length] - PRINT_CHAR_START;                              // Takes key_string @ i value, mods by the key length for wrap around
                                                                                                            // subtracts the value of ' ' (32) to determine shift
                character = ((character - PRINT_CHAR_START) + shift) % PRINT_RANGE + PRINT_CHAR_START;      // starts with character value and subtracts 32, adds shift value. 
                                                                                                            // then that whole value is modded by the print range for wrap around
                                                                                                            // and start is added back
                key_index++;
            }
            buffer[i] = character;
        }
        write(1, buffer, num_bytes_read);
    }
}
