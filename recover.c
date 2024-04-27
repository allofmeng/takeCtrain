#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
FILE* create_new_file(char* filename, uint8_t* buffer, int size, int* count);
bool is_jpg(uint8_t *buffer);
int main(int argc, char *argv[])

{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    int Blocksize = 512;

    // determine file size : card store memeory in blocks of 512 bytes.

    // create buffer so it can be write in
    uint8_t *buffer = malloc(Blocksize);
    if (buffer == NULL)
        return 1;

    // While there's still data left to read from the memory card
    int count = 0;
    char filename[8];
    FILE *newjpg = NULL;
    while (fread(buffer, 1, 512, card) == 512)
    {
        // conditional check for jpg header
        if (is_jpg(buffer) == 1)
        { // if found writie into new jpg file
            
            if (newjpg != NULL)
            {
                fclose(newjpg);
            }
            newjpg = create_new_file(filename, buffer, Blocksize, &count);

        }
        else if (is_jpg(buffer) ==
                 0) // only checked when previous if is false, header not found, continue write
        {
            if (newjpg != NULL) // check if newjpg not NULL
            {
                fwrite(buffer, 1, Blocksize, newjpg);
            }
        }
    }

    fclose(newjpg);
    free(buffer);
    fclose(card);
}

bool is_jpg(uint8_t *buffer) // boolean for jpg or not
{
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}

FILE* create_new_file(char* filename, uint8_t* buffer, int size, int* count)
{
    sprintf(filename, "%03i.jpg", *count); // Generate the filename using the count
    FILE* newjpg = fopen(filename, "w");
    if (newjpg == NULL)
    {
        printf("Error creating file: %s\n", filename);
        return NULL;
    }
    fwrite(buffer, 1, size, newjpg); // Write the buffer to the new JPEG file
    (*count)++; // Increment the count for the next file
    return newjpg;
}
