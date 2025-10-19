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
#define OPTIONS "edc:x:hD"
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
void caesar_encrypt(char *buffer, size_t plain_text_length, char *key_string);
void xor_encode(char *buffer, size_t plain_text_length, char *key_string);

int main(int argc, char *argv[])
{
    bool enc_dec = true;                                                    // if enc_dec == true: encrypt was last to be seen (it is also the default value), else decrypt was last to be seen
    bool diagnostic = false;                                                // Indicates if diagnostic flag is set
    char *cae_key_string = NULL;                                            // Stores caesar key string after getopt parsing 
    char *xor_key_string = NULL;                                            // Stores xor key string after getopt parsing 
    char buffer[BUFFER_SIZE];                                               // Read in buffer
    size_t plain_text_length;                                               // Length of plain text bytes read

    NOISY_DEBUG_PRINT;

    // getopt structure
    {
        int opt = 0;                                                        // getopt option variable

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
            NOISY_DEBUG_PRINT;
            switch(opt)
            {
                // encrypt
                case 'e':
                    enc_dec = true;
                    break;
                // decrypt
                case 'd':
                    enc_dec = false;
                    break;
                // caesar cipher encrypt key
                case 'c':
                    cae_key_string = optarg;
                    break;
                // xor cipher encrypt key
                case 'x':
                    xor_key_string = optarg;
                    break;
                // help (no argument required)
                // UPDATE LATER
                case 'h':
                    printf("helpful info\n");
                    break;
                // Diagnostic info
                case 'D':
                    diagnostic = true;
                    printf("Diagnostic info\n");
                    break;
                default:
                    break;
            }
        }
    }

        NOISY_DEBUG_PRINT;
        while ((plain_text_length = read(0, buffer, BUFFER_SIZE)) > 0)
        {
            if (enc_dec)
            {
                if (cae_key_string)
                {
                    caesar_encrypt(buffer, plain_text_length, cae_key_string);
                }
                if (xor_key_string)
                {
                    xor_encode(buffer, plain_text_length, xor_key_string);
                }

            }
            else
            {
                printf("uffffff\n");
            }
            write(1, buffer, plain_text_length);
        }

    return EXIT_SUCCESS;
}


void caesar_encrypt(char *buffer, size_t plain_text_length, char *key_string)
{
    char character;
    size_t key_index = 0;
    size_t key_length = strlen(key_string);
    int shift = 0;

    NOISY_DEBUG_PRINT;
    for (size_t i = 0; i < plain_text_length; i++)
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
}


void xor_encode(char *buffer, size_t plain_text_length, char *key_string)
{
        size_t key_index = 0;
        size_t key_length = strlen(key_string);

        for (size_t i = 0; i < plain_text_length; i++)
        {
            buffer[i] = buffer[i] ^ (key_string[key_index % key_length]);
            key_index++;
        }
}