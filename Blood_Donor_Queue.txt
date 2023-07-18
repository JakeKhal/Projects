#include <stdio.h>   /* printf */
#include <stdlib.h>  /* malloc */
#include <string.h>  /* strcmp */

#define QUEUE_SIZE 12  
#define BLOOD_TYPES 4
#define LINE_LENGTH 80

struct queue
{
    char *strings[QUEUE_SIZE];
    int population;
    int front;
    int back;
};
typedef struct queue Queue;

void initializeQueue (Queue *q)
{
    q->population = 0;
    q->front = 0;
    q->back = 0;
}

void enqueue(char *person, Queue *q)
{
	
    if (q->population == QUEUE_SIZE) { exit(EXIT_FAILURE); }

    q->strings[q->back] = strdup(person);
    (q->population)++;
    (q->back) = (q->back + 1) % QUEUE_SIZE;
}

char *dequeue(Queue *q)
{
    if (q->population == 0) { exit(EXIT_FAILURE); }

    (q->population) --;
    char *dequeued = q->strings[q->front];
    (q->front) = (q->front + 1) % QUEUE_SIZE;

    return dequeued;
}

int check_empty(Queue *q) 
{
	if (q->population == 0) 
		return 0;
	return 1;
}

int isDonorToRecipient(char *donor, char *recipient)
{
  if (strcmp(donor, "O") == 0 || strcmp(donor, recipient) == 0)
    return 1;
  if (strcmp(donor, "A") == 0 && strcmp(recipient, "AB") == 0)
    return 1;
  if (strcmp(donor, "B") == 0 && strcmp(recipient, "AB") == 0)
    return 1;
  return 0;
}


void printQueue(struct queue *q)
{
  printf("Printing queue %p\n", q);
  printf("\tThe index for the front of the queue is %d\n", q->front);
  printf("\tThe index for the back of the queue is %d\n", q->back);
  if (q->population == 0)
  {
    printf("\tThe queue is empty.\n");
  }
  else
  {
    for (int i = 0; i < q->population; i++)
    {
      int index = (q->front + i) % QUEUE_SIZE;
      printf("\t\tEntry[%d]: \"%s\"\n", index, q->strings[index]);
    }
  }
}

void prettyPrintQueue(struct queue *q, char *label, char *type)
{
  if (q->population == 0)
  {
    printf("No unmatched entries for %s (%s)\n", label, type);
  }
  else
  {
    printf("Unmatched %s (%s):\n", label, type);
    for (int i = 0; i < q->population; i++)
    {
      int index = (q->front + i) % QUEUE_SIZE;
      printf("%s\n", q->strings[index]);
    }
  }
}

int get_blood(char *line, char *blood) 
{
	int index = 2;

        while (line[index] != ':') {
        	blood[index-2] = line[index];
                index ++;
                                    }
                index ++;
                return index;
}


void get_name(char *line, int index, char *name) 
{
	int i = 0;
	while (line[index] != '\n') {
        name[i] = line[index];
        index++;
        i++;
                                     }           
}


void line_slicer(char *line, char *status, char *blood, char *name)
{
	status[0] = line[0];

        if (status[0] == 'S') {
        	get_name(line, 2, name);
                                        }
        if (status[0] == 'R' || status[0] == 'D') {
                int index = get_blood(line, blood);
                get_name(line, index, name);
                                                   }
}

                                 

int main(int argc, char **argv)
{

        FILE *f = fopen(argv[argc-1], "r");
        if (f == NULL)
        {
                fprintf(stderr, "Unable to open file");
                exit(EXIT_FAILURE);
        }
	 
	char *types[BLOOD_TYPES] = {"AB", "B", "A", "O"};
	struct queue *donors[BLOOD_TYPES];
 	struct queue *recipients[BLOOD_TYPES];
 	struct queue *surgeons = malloc(sizeof (struct queue));

	for (int i = 0; i < 4; i++) {
		donors[i] = malloc(sizeof(Queue));
		initializeQueue(donors[i]);
				     }	

	for (int i = 0; i < 4; i++) {
                recipients[i] = malloc(sizeof(Queue));
                initializeQueue(recipients[i]);
                                     }

	initializeQueue(surgeons);

	
	char line[LINE_LENGTH];
        while (fgets(line, LINE_LENGTH, f))
        {
        
	char status[2] = " ";
	char blood[3] = " ";
        char name[20] = " ";
	
	line_slicer(line, status, blood, name);
	
	int compatible_exists = 0;

	int compatible_type = -1;
	//AB B A O = 0 1 2 3
	int blood_num = -1;

	if (blood[0] == 'A' && blood[1] == 'B') blood_num = 0;
	else if (blood[0] == 'B') blood_num = 1;
	else if (blood[0] == 'A') blood_num = 2;
	else if (blood[0] == 'O') blood_num = 3;	

	//RECIPIENTS
	if (strcmp(status, "R") == 0) {

		if (blood[0] == 'A' && blood[1] == 'B') {
			if (check_empty(donors[0])==1) {compatible_type = 0; compatible_exists = 1;}

			else if (check_empty(donors[1])==1) {compatible_type = 1; compatible_exists = 1;}

			else if (check_empty(donors[2])==1) {compatible_type = 2; compatible_exists = 1;}

			else if (check_empty(donors[3])==1) {compatible_type = 3; compatible_exists = 1; }
				   }


		else if (blood[0] == 'B') {
			if (check_empty(donors[1])==1) {compatible_type = 1; compatible_exists = 1;}
				   
			else if (check_empty(donors[3])==1) {compatible_type = 3; compatible_exists = 1; }
				   }

		else if (blood[0] == 'A') {
			if (check_empty(donors[2])==1) {compatible_type = 2; compatible_exists = 1; }

			else if (check_empty(donors[3])==1) {compatible_type = 3; compatible_exists = 1; }
				   }

		else if (blood[0] == 'O') {
			if (check_empty(donors[3])==1) {compatible_type = 3; compatible_exists = 1; }
				  }

 
		if (check_empty(surgeons) == 0 || compatible_exists == 0) 
			enqueue(name, recipients[blood_num]); 
		else {
			if (compatible_exists == 1 && (check_empty(surgeons) == 1) ) {
				char *donor = dequeue(donors[compatible_type]);
				char *surgeon = dequeue(surgeons);
				printf( "MATCH: %s donates to %s via Dr. %s\n",
                                        donor,    name,   surgeon);				    
										 }

	            }	      
				}



	//DONORS
	if (strcmp(status, "D") == 0) {

		if (blood[0] == 'A' && blood[1] == 'B') {
                        if (check_empty(recipients[0])==1) {compatible_type = 0; compatible_exists = 1;}
                                   }


                else if (blood[0] == 'B') {
                        if (check_empty(recipients[1])==1) {compatible_type = 1; compatible_exists = 1;}

                        else if (check_empty(recipients[0])==1) {compatible_type = 0; compatible_exists = 1; }
                                   }

                else if (blood[0] == 'A') {
                        if (check_empty(recipients[2])==1) {compatible_type = 2; compatible_exists = 1; }

                        else if (check_empty(recipients[0])==1) {compatible_type = 0; compatible_exists = 1; }
                                   }

                else if (blood[0] == 'O') {
                        if (check_empty(recipients[0])==1) {compatible_type = 0; compatible_exists = 1; }
                                  
			else if (check_empty(recipients[1])==1) {compatible_type = 1; compatible_exists = 1; }
                        
			else if (check_empty(recipients[2])==1) {compatible_type = 2; compatible_exists = 1; }
                        
			else if (check_empty(recipients[3])==1) {compatible_type = 3; compatible_exists = 1; }
					}

		
		if (check_empty(surgeons) == 0 || compatible_exists == 0)
                        enqueue(name, donors[blood_num]);
                else {
                        if (compatible_exists == 1 && (check_empty(surgeons) == 1) ) {
                                char *recipient = dequeue(recipients[compatible_type]);
                                char *surgeon = dequeue(surgeons); 
				printf( "MATCH: %s donates to %s via Dr. %s\n", name, recipient, surgeon);  }

                        else { enqueue(name, donors[blood_num]); }
                    }
					}


	//SURGEONS
	if (strcmp(status, "S") == 0) {

		int donor_blood = -1;
		int recipient_blood = -1;
		int match_exists = 0;
		
		//Donor - Recepients(s)
		//AB - AB, B, A, O		
		if (check_empty(recipients[0]) == 1 && check_empty(donors[0]) == 1) {
			recipient_blood = 0;
			donor_blood = 0; 
			match_exists = 1;}

		else if (check_empty(recipients[0]) == 1 && check_empty(donors[1]) == 1) {
                        recipient_blood = 0;
                        donor_blood = 1; 
			match_exists = 1; }

		else if (check_empty(recipients[0]) == 1 && check_empty(donors[2]) == 1) {
                        recipient_blood = 0;
                        donor_blood = 2; 
			match_exists = 1; }
	
		else if (check_empty(recipients[0]) == 1 && check_empty(donors[3]) == 1) {
                        recipient_blood = 0;
                        donor_blood = 3; 
			match_exists = 1; }

		//B - B, O
		else if (check_empty(recipients[1]) == 1 && check_empty(donors[1]) == 1) {
                        recipient_blood = 1;
                        donor_blood = 1; 
			match_exists = 1;}

		else if (check_empty(recipients[1]) == 1 && check_empty(donors[3]) == 1) {
                        recipient_blood = 1;
                        donor_blood = 3; 
			match_exists = 1;}
		
		//A - A, O
		else if (check_empty(recipients[2]) == 1 && check_empty(donors[2]) == 1) {
                        recipient_blood = 2;
                        donor_blood = 2; 
			match_exists = 1;}

		else if (check_empty(recipients[2]) == 1 && check_empty(donors[3]) == 1) {
                        recipient_blood = 2;
                        donor_blood = 3; 
			match_exists = 1; }

		//O - O
		else if (check_empty(recipients[3]) == 1 && check_empty(donors[3]) == 1) {
                        recipient_blood = 3;
                        donor_blood = 3; 
			match_exists = 1;}


		
		if (match_exists == 1) {

			char *donor = dequeue(donors[donor_blood]);
			char *recipient = dequeue(recipients[recipient_blood]);
			printf( "MATCH: %s donates to %s via Dr. %s\n", donor, recipient, name);
					}
		else {enqueue(name, surgeons);}

				      }

        }
        fclose(f);
 

	for (int r = 0; r < BLOOD_TYPES; r++)
		prettyPrintQueue(recipients[r], "recipients", types[r]);

	for (int d = 0; d < BLOOD_TYPES; d++)
		prettyPrintQueue(donors[d], "donors", types[d]);

	prettyPrintQueue(surgeons, "surgeons", "type-agnostic");


  free(surgeons);
  for (int i = 0; i<4; i++) {
	free(donors[i]);
	free(recipients[i]); }

  return EXIT_SUCCESS;

}


