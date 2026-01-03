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

#define OPTIONS "edc:x:hD"
#define BUFFER_SIZE 1000000
#define PRINT_CHAR_START 32
#define PRINT_CHAR_END 126
#define PRINT_RANGE (PRINT_CHAR_END - PRINT_CHAR_START + 1)


// Prototypes
void caesar_encrypt(char *buffer, size_t plain_text_length, char *key_string, bool diagnostic, bool encrypt);
void xor_encode(char *buffer, size_t plain_text_length, char *key_string, bool diagnostic);


int main(int argc, char *argv[])
{
    bool enc_dec = true;                                                    // if enc_dec == true: encrypt was last to be seen (it is also the default value), else decrypt was last to be seen
    bool diagnostic = false;                                                // Indicates if diagnostic flag is set
    bool help = false;
    char *cae_key_string = NULL;                                            // Stores caesar key string after getopt parsing 
    char *xor_key_string = NULL;                                            // Stores xor key string after getopt parsing 
    char buffer[BUFFER_SIZE];                                               // Read in buffer
    size_t plain_text_length;                                               // Length of plain text bytes read


    // getopt structure
    {
        int opt = 0;                                                        // getopt option variable

        while ((opt = getopt(argc, argv, OPTIONS)) != -1)
        {
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
                case 'h':
                    help = true;
                    break;
                // Diagnostic info
                case 'D':
                    diagnostic = true;
                    break;
                default:
                    break;
            }
        }
    }
        if (help)
        {
            printf("-e\tencrypt text(this is the default)\n");
            printf("-d\tdecrypt text\n");
            printf("-c str\tstring to use for caesar cipher algorithm (default NULL)\n");
            printf("-x str\tstring to use for xor cipher algorithm (default NULL)\n");
            printf("-D\tenable diagnostic output\n");
            printf("-h show help and exit\n");
            exit(EXIT_SUCCESS);
        }

        while ((plain_text_length = read(0, buffer, BUFFER_SIZE)) > 0)
        {
            if (enc_dec)
            {
                if (cae_key_string)
                {
                    caesar_encrypt(buffer, plain_text_length, cae_key_string, diagnostic, enc_dec);
                }
                if (xor_key_string)
                {
                    xor_encode(buffer, plain_text_length, xor_key_string, diagnostic);
                }

            }
            else
            {
                if (xor_key_string)
                {
                    xor_encode(buffer, plain_text_length, xor_key_string, diagnostic);
                }
                if (cae_key_string)
                {
                    caesar_encrypt(buffer, plain_text_length, cae_key_string, diagnostic, enc_dec);
                }

            }
            write(1, buffer, plain_text_length);
        }

    return EXIT_SUCCESS;
}


void caesar_encrypt(char *buffer, size_t plain_text_length, char *key_string, bool diagnostic, bool encrypt)
{
    char character;
    size_t key_index = 0;
    size_t key_length = strlen(key_string);
    int shift = 0;

    if (diagnostic)
        fprintf(stderr, "Caesar key: %s\n", key_string);

    for (size_t i = 0; i < plain_text_length; i++)
    {
        character = buffer[i];
        if (isprint(character))                                                                         // only runs if the character is printable
        {
            shift = key_string[key_index % key_length] - PRINT_CHAR_START;                              // Takes key_string @ i value, mods by the key length for wrap around
            if (!encrypt)
                shift = -shift;
                                                                                                        // subtracts the value of ' ' (32) to determine shift
            character = ((character - PRINT_CHAR_START) + shift + PRINT_RANGE) % PRINT_RANGE + PRINT_CHAR_START;      // starts with character value and subtracts 32, adds shift value. 
                                                                                                        // then that whole value is modded by the print range for wrap around
                                                                                                        // and start is added back
            if (diagnostic)
            {
                fprintf(stderr, "ce\tshift char %c\tshift num %d\tchar %c -> %c\n", key_string[key_index % key_length], shift, buffer[i], character);
            }
            key_index++;
        }
        buffer[i] = character;
    }
}


void xor_encode(char *buffer, size_t plain_text_length, char *key_string, bool diagnostic)
{
        size_t key_index = 0;
        size_t key_length = strlen(key_string);
        char plain_text;
        char key_char;

        if (diagnostic)
            fprintf(stderr, "xor key: %s\n", key_string);
        for (size_t i = 0; i < plain_text_length; i++)
        {
            plain_text = buffer[i];
            key_char = key_string[key_index % key_length];
            buffer[i] = plain_text ^ key_char;
            if (diagnostic)
                fprintf(stderr, "xe\txor char %c \t0x%x\tplain \t0x%x \t-> \t0x%x\n", key_char, key_char, plain_text, buffer[i]);

            key_index++;
        }
}