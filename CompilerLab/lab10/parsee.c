#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_MNEMONICS 30
#define MAX_LITERALS 10
#define MAX_SYMBOLS 10
#define MAX_POOLS 10
#define MAX_LINES 100

typedef struct
{
    char code[10];
    char category[3];
    char machineRep[10];
    int size;
} Opcode;

typedef struct
{
    char value[10];
    int location;
} LiteralEntry;

typedef struct
{
    char name[10];
    int location;
} SymbolEntry;

typedef struct
{
    int index;
} LiteralPool;

// Display functions for each table
void displayIntermediateCode(char ic[MAX_LINES][50], char assembly[MAX_LINES][50], int addresses[MAX_LINES], int totalLines)
{
    printf("\n+----------------------+------------+--------------------------------+\n");
    printf("| %-20s | %-10s | %-30s |\n", "SRC", "LC", "IC");
    printf("+----------------------+------------+--------------------------------+\n");
    for (int i = 0; i < totalLines; i++)
    {
        printf("| %-20s | %-10d | %-30s |\n", assembly[i], addresses[i], ic[i]);
    }
    printf("+----------------------+------------+--------------------------------+\n");
}

void displayLiteralTable(LiteralEntry literals[], int literalCount)
{
    printf("\nLiteral Table:\n");
    printf("+-------+-----------------+------------+\n");
    printf("| Index | Literal         | Address    |\n");
    printf("+-------+-----------------+------------+\n");
    for (int i = 0; i < literalCount; i++)
    {
        printf("| %-5d | %-15s | %-10d |\n", i, literals[i].value, literals[i].location);
    }
    printf("+-------+-----------------+------------+\n");
}

void displaySymbolTable(SymbolEntry symbols[], int symbolCount)
{
    printf("\nSymbol Table:\n");
    printf("+-------+-----------------+------------+\n");
    printf("| Index | Symbol          | Address    |\n");
    printf("+-------+-----------------+------------+\n");
    for (int i = 0; i < symbolCount; i++)
    {
        printf("| %-5d | %-15s | %-10d |\n", i, symbols[i].name, symbols[i].location);
    }
    printf("+-------+-----------------+------------+\n");
}

void displayPoolTable(LiteralPool pools[], int poolCount)
{
    printf("\nLiteral Pool Table:\n");
    printf("+----------+---------------------+\n");
    printf("| Pool No. | Literal Start Index |\n");
    printf("+----------+---------------------+\n");
    for (int i = 0; i < poolCount; i++)
    {
        printf("| %-8d | %-19d |\n", i, pools[i].index);
    }
    printf("+----------+---------------------+\n");
}

// Get the index of a given opcode
int getOpcodeIndex(Opcode opcodes[], char *code, int count)
{
    for (int i = 0; i < count; i++)
    {
        if (strcmp(opcodes[i].code, code) == 0)
        {
            return i;
        }
    }
    return -1;
}

// Process the assembly code and populate intermediate code tables
void processAssembly(Opcode opcodes[], LiteralEntry literals[], SymbolEntry symbols[], LiteralPool pools[],
                     char ic[MAX_LINES][50], char assembly[MAX_LINES][50], int addresses[MAX_LINES],
                     int *literalCount, int *symbolCount, int *poolCount, int *lineCount)
{

    int currentLocation = 0;
    char line[100], code[10], operand1[10], operand2[10];

    FILE *file = fopen("input.txt", "r");
    if (!file)
    {
        printf("Error opening file!\n");
        return;
    }

    // Initialize first pool index
    pools[*poolCount].index = *literalCount;
    (*poolCount)++;

    // Read lines from input file
    while (fgets(line, sizeof(line), file))
    {
        sscanf(line, "%s %s %s", code, operand1, operand2);
        int opcodeIndex = getOpcodeIndex(opcodes, code, MAX_MNEMONICS);

        if (opcodeIndex != -1)
        {
            addresses[*lineCount] = currentLocation;

            // Handle different opcodes
            if (strcmp(opcodes[opcodeIndex].code, "START") == 0)
            {
                currentLocation = atoi(operand1);
                sprintf(assembly[*lineCount], "%s %s", code, operand1);
                sprintf(ic[(*lineCount)++], "(AD, 01) (C, %d)", currentLocation);
            }
            else if (strcmp(opcodes[opcodeIndex].code, "LTORG") == 0)
            {
                for (int i = pools[*poolCount - 1].index; i < *literalCount; i++)
                {
                    literals[i].location = currentLocation++;
                }
                pools[(*poolCount)++].index = *literalCount;
                sprintf(assembly[*lineCount], "%s", code);
                sprintf(ic[(*lineCount)++], "(AD, 05)");
            }
            else if (strcmp(opcodes[opcodeIndex].code, "END") == 0)
            {
                sprintf(assembly[*lineCount], "%s", code);
                sprintf(ic[(*lineCount)++], "(AD, 02)");
            }
            else if (operand2[0] == '=')
            {
                strcpy(literals[*literalCount].value, operand2);
                sprintf(assembly[*lineCount], "%s %s, %s", code, operand1, operand2);
                sprintf(ic[(*lineCount)++], "(IS, %s) (%s) (L, %d)", opcodes[opcodeIndex].machineRep, operand1, *literalCount);
                literals[*literalCount].location = currentLocation++;
                (*literalCount)++;
            }
        }
    }
    fclose(file);
}

int main()
{
    // Opcode table initialization
    Opcode opcodes[MAX_MNEMONICS] = {
        {"STOP", "IS", "00", 1}, {"ADD", "IS", "01", 1}, {"SUB", "IS", "02", 1}, {"MOVER", "IS", "04", 1}, {"MOVEM", "IS", "05", 1}, {"LTORG", "AD", "05", 0}, {"START", "AD", "01", 0}, {"END", "AD", "02", 0}
        // Additional opcodes can be added here
    };

    LiteralEntry literals[MAX_LITERALS];
    SymbolEntry symbols[MAX_SYMBOLS];
    LiteralPool pools[MAX_POOLS];

    char intermediateCode[MAX_LINES][50];
    char assemblyCode[MAX_LINES][50];
    int lineAddresses[MAX_LINES];

    int literalCount = 0, symbolCount = 0, poolCount = 0, lineCount = 0;

    processAssembly(opcodes, literals, symbols, pools, intermediateCode, assemblyCode, lineAddresses,
                    &literalCount, &symbolCount, &poolCount, &lineCount);

    // Display tables
    displayIntermediateCode(intermediateCode, assemblyCode, lineAddresses, lineCount);
    displayLiteralTable(literals, literalCount);
    displaySymbolTable(symbols, symbolCount);
    displayPoolTable(pools, poolCount);

    return 0;
}
