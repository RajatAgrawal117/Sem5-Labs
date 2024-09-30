#include <stdio.h>
#include <string.h>

#define MAX_STACK_SIZE 100
#define NUM_OPERATORS 4

const char operators[NUM_OPERATORS][10] = {"id", "+", "*", "$"};

char precedence_table[NUM_OPERATORS][NUM_OPERATORS] = {
    {' ', '>', '>', '>'},
    {'<', '>', '<', '>'},
    {'<', '>', '>', '>'},
    {'<', '<', '<', ' '}
};

int findOperatorIndex(const char *op)
{
    for (int i = 0; i < NUM_OPERATORS; i++)
    {
        if (strcmp(operators[i], op) == 0)
        {
            return i;
        }
    }
    return -1;
}

void printStack(char stack[MAX_STACK_SIZE][10], int top)
{
    printf("Stack: ");
    for (int i = 0; i <= top; i++)
    {
        printf("%s ", stack[i]);
    }
    printf("\n");
}

int main()
{
    char stack[MAX_STACK_SIZE][10];
    int top = 0;

    strcpy(stack[top], "$");

    char input[MAX_STACK_SIZE];
    printf("Enter the input string (e.g., id+id*id$): ");
    fgets(input, MAX_STACK_SIZE, stdin);
    input[strcspn(input, "\n")] = '\0';

    const char *currentInput = input;
    int lastWasId = 0;

    printf("\nProcessing input: %s\n", input);

    while (*currentInput != '\0')
    {
        char topOfStack[10];
        strcpy(topOfStack, stack[top]);

        char currentSymbol[10];
        if (strncmp(currentInput, "id", 2) == 0)
        {
            strcpy(currentSymbol, "id");
            currentInput += 2;

            if (lastWasId)
            {
                printf("Error: Consecutive ids found without an operator\n");
                return 0;
            }

            lastWasId = 1;
        }
        else
        {
            snprintf(currentSymbol, sizeof(currentSymbol), "%c", *currentInput);
            currentInput++;

            if (!lastWasId && strcmp(currentSymbol, "id") != 0 && strcmp(currentSymbol, "$") != 0)
            {
                printf("Error: Consecutive operators found without an operand\n");
                return 0;
            }

            lastWasId = 0;
        }

        printf("\nCurrent symbol: %s\n", currentSymbol);
        printStack(stack, top);

        int topIndex = findOperatorIndex(topOfStack);
        int currentIndex = findOperatorIndex(currentSymbol);

        if (currentIndex == -1)
        {
            printf("Error: Invalid symbol found\n");
            return 0;
        }

        char precedence = precedence_table[topIndex][currentIndex];
        printf("Precedence between top of stack '%s' and current symbol '%s': %c\n", topOfStack, currentSymbol, precedence);

        if (precedence == '<' || precedence == ' ')
        {
            top++;
            strcpy(stack[top], currentSymbol);
            printf("Action: Push '%s' onto the stack\n", currentSymbol);
        }
        else if (precedence == '>')
        {
            printf("Action: Reduce (Pop stack until precedence is no longer greater)\n");
            while (top > 0 && precedence_table[findOperatorIndex(stack[top])][currentIndex] == '>')
            {
                printf("Popping '%s' from the stack\n", stack[top]);
                top--;
            }
            top++;
            strcpy(stack[top], currentSymbol);
            printf("Action: Push '%s' onto the stack\n", currentSymbol);
        }
        else
        {
            printf("Error: Invalid precedence relation\n");
            return 0;
        }

        printStack(stack, top);
    }

    while (top > 0)
    {
        printf("Popping '%s' from the stack\n", stack[top]);
        top--;
    }

    if (top == 0 && strcmp(stack[top], "$") == 0)
    {
        printf("\nParsing completed successfully\n");
        return 1;
    }
    else
    {
        printf("\nParsing failed\n");
        return 0;
    }
}
