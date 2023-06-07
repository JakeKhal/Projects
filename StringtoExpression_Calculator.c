#include <stdio.h>
#include <stdlib.h>

typedef enum
{
   ADD,
   MULT,
   SUBTRACT,
   DIV,
   UNSUPPORTED
} MathOperation;

void IssueBadNumberError()
{
    printf("The string does not represent a floating point number.\n");
    exit(EXIT_FAILURE);
}
void IssueBadOperationError()
{
    printf("The string does not represent a valid operation.\n");
    exit(EXIT_FAILURE);
}


MathOperation GetOperation(char *op)
{   	
    if ((op[1]) != '\0')
	IssueBadOperationError();

    if (*op == '+')
	return ADD;
    else if (*op == '-')
	return SUBTRACT;
    else if (*op == 'x')
	return MULT;
    else if (*op == '/')
	return DIV;
    else
	return UNSUPPORTED;
}

int string_length(char *str) {
        int len = 0;
        for (int x = 0; str[x] != '\0'; x++) {
                len++;                       }
        return len;
                            }

int power(int num) {
	int result = 1;
	while (num > 0) {
		result *= 10;
		num--; }
	return result;   }


double StringToDouble(char *str) 
{
    double value = 0.0;

    int str_place = 0;

    int negative_val = 0;
    if (str[0] == '-') negative_val=1;
	
	
    int before_decimal = 0;

    int decimal_present = 0;
	while (str[str_place] != '\0') {
		if (str[str_place] == '.') { decimal_present = 1; }
		str_place++;	       }

	
    str_place = 0;

    while (str[str_place] != '.' && str[str_place] != '\0') {
	before_decimal++;
	str_place++;	  }

    for (int c = before_decimal-1; c >= negative_val; c--) {
	if (0 > str[c]-'0' || str[c]-'0' > 9) {
			IssueBadNumberError();              }
	value += (str[c]-'0') * (power(before_decimal - c- 1)); }

 
if (decimal_present == 1) {
    int after_decimal = 0;
    double decimal_value = 0.0; 	   

    while (str[str_place+1] != '\0') { 
        after_decimal++;
        str_place++;
				     }

	for (int d = after_decimal+before_decimal; d>before_decimal; d--) {
		if (0 > str[d]-'0' || str[d]-'0' > 9) {
                        IssueBadNumberError();              }

		decimal_value += (str[d]-'0') * (power(after_decimal+before_decimal- d));	
				}
	decimal_value /= (power(after_decimal)); 									    
			
	value += decimal_value;
			}

    if (negative_val == 1)
	value /= -1;

return value;

}


int main(int argc, char *argv[])
{
    double v = StringToDouble(argv[1]);
    MathOperation op = GetOperation(argv[2]);
    double v2 = StringToDouble(argv[3]);
    double result = 0.;

    switch (op)
    
     {
	case ADD:
         result = (double)v+(double)v2;
         break;
	
	case SUBTRACT:
	 result = (double)v-(double)v2;
	 break;
	
	case MULT:
	 result = (double)v*(double)v2;
         break;
	
	case DIV:
	 result = (double)v/(double)v2;
	 break;
	
	case UNSUPPORTED:
	 IssueBadOperationError();
	 break;
    }
   
    printf("%d\n", (int) result);
    
}
