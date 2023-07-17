#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void main (int argc, char *argv[]){


FILE *file;
int buff_size;
char *buffer;

file = fopen(argv[1], "r");

if (file == NULL) {
	printf("%s is not a valid file.", argv[1]);
	exit(1);  }


fseek(file, 0, SEEK_END);
buff_size = ftell(file);
fseek(file, 0, SEEK_SET);

buffer = malloc(buff_size);
fread(buffer, sizeof(char), buff_size, file);
	  	
fclose(file);



int count = 0;
int *match_words = malloc((argc-2)*sizeof(int));

for (int x = 0; x<argc-2; x++)
	match_words[x] = 0;

for (int c=0; c<=strlen(buffer); c++) {
	
	char tmp_word[100];
	tmp_word[count] = buffer[c];

	if (buffer[c] == '.' || buffer[c] == ',' || buffer[c] == ' ' || buffer[c] == '\n') { 
		tmp_word[count] = '\0'; 

		for (int a = 2; a<argc; a++) {
			if (strlen(tmp_word) == strlen(argv[a])) {
				if (strncmp(tmp_word, argv[a], strlen(argv[a])) == 0) {
					match_words[a-2] += 1; 
								  }}
					     }
		count = 0;								   }
	else
	count += 1;
				      }
for (int w = 2; w<argc; w++)
	printf("The word \"%s\" occurs %d times.\n", argv[w], match_words[w-2]);


				 } 



