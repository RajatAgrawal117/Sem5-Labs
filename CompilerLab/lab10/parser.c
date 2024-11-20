#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_MNEMONICS 30
#define MAX_LITERALS 10
#define MAX_SYMBOLS 10
#define MAX_POOLS 10
#define MAX_LINES 100

typedef struct {
    char code[10];
    char category[3];
    char machineRep[10];
    int size;
} Opcode;

typedef struct {
    char value[10];
    int location;
} LiteralEntry;

typedef struct {
    char name[10];
    int location;
} SymbolEntry;

typedef struct {
    int index;
} LiteralPool;

void displayIntermediateCode(char ic[MAX_LINES][50], char assembly[MAX_LINES][50], int addresses[MAX_LINES], int totalLines) {
    printf("\n+----------------------+------------+--------------------------------+\n");
    printf("| %-20s | %-10s | %-30s |\n", "SRC", "LC", "IC");
    printf("+----------------------+------------+--------------------------------+\n");

    for (int i = 0; i < totalLines; i++) {
        printf("| %-20s | %-10d | %-30s |\n", assembly[i], addresses[i], ic[i]);
    }

    printf("+----------------------+------------+--------------------------------+\n");
}

void displayLiteralTable(LiteralEntry literals[], int literalCount) {
    printf("\n+-------+-----------------+------------+\n");
    printf("| %-5s | %-15s | %-10s |\n", "Index", "Literal", "Address");
    printf("+-------+-----------------+------------+\n");

    for (int i = 0; i < literalCount; i++) {
        printf("| %-5d | %-15s | %-10d |\n", i, literals[i].value, literals[i].location);
    }

    printf("+-------+-----------------+------------+\n");
}

void displaySymbolTable(SymbolEntry symbols[], int symbolCount) {
    printf("\n+-------+-----------------+------------+\n");
    printf("| %-5s | %-15s | %-10s |\n", "Index", "Symbol", "Address");
    printf("+-------+-----------------+------------+\n");

    for (int i = 0; i < symbolCount; i++) {
        printf("| %-5d | %-15s | %-10d |\n", i, symbols[i].name, symbols[i].location);
    }

    printf("+-------+-----------------+------------+\n");
}

void displayPoolTable(LiteralPool pools[], int poolCount) {
    printf("\n+----------+---------------------+\n");
    printf("| %-5s | %-15s |\n", "Pool No.", "Literal Start Index");
    printf("+----------+---------------------+\n");

    for (int i = 0; i < poolCount; i++) {
        printf("| %-8d | %-19d |\n", i, pools[i].index);
    }

    printf("+----------+---------------------+\n");
}

int getOpcodeIndex(Opcode opcodes[], char *code, int count) {
    for (int i = 0; i < count; i++) {
        if (strcmp(opcodes[i].code, code) == 0) {
            return i;
        }
    }
    return -1;
}

int getSymbolIndex(SymbolEntry symbols[], char *name, int count) {
    for (int i = 0; i < count; i++) {
        if (strcmp(symbols[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

int addSymbolEntry(SymbolEntry symbols[], char *name, int *symbolCount, int location) {
    strcpy(symbols[*symbolCount].name, name);
    symbols[*symbolCount].location = location;
    (*symbolCount)++;
    return *symbolCount - 1;
}

int isValidSymbolName(char *str) {
    return !isdigit(str[0]);
}

int calculateOperandAddress(char *operand, SymbolEntry symbols[], int symbolCount) {
    char symbol[10];
    int offset = 0;

    if (sscanf(operand, "%[^+]+%d", symbol, &offset) == 2) {
        int symbolIndex = getSymbolIndex(symbols, symbol, symbolCount);
        if (symbolIndex != -1) {
            return symbols[symbolIndex].location + offset;
        }
    } else if (isdigit(operand[0])) {
        return atoi(operand);
    } else {
        int symbolIndex = getSymbolIndex(symbols, operand, symbolCount);
        if (symbolIndex != -1) {
            return symbols[symbolIndex].location;
        }
    }

    return -1;
}

void processAssembly(Opcode opcodes[], LiteralEntry literals[], SymbolEntry symbols[], LiteralPool pools[], 
                     char ic[MAX_LINES][50], char assembly[MAX_LINES][50], int addresses[MAX_LINES], 
                     int *literalCount, int *symbolCount, int *poolCount, int *lineCount) {

    int currentLocation = 0;
    char line[100], code[10], operand1[10], operand2[10];

    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Error opening file!\n");
        return;
    }

    pools[*poolCount].index = *literalCount;
    (*poolCount)++;

    while (fgets(line, sizeof(line), file)) {
        strcpy(operand1, "");
        strcpy(operand2, "");

        sscanf(line, "%s %s %s", code, operand1, operand2);

        int opcodeIndex = getOpcodeIndex(opcodes, code, MAX_MNEMONICS);
        if (opcodeIndex != -1) {
            addresses[*lineCount] = currentLocation;

            if (strcmp(opcodes[opcodeIndex].code, "START") == 0) {
                currentLocation = atoi(operand1);
                sprintf(assembly[*lineCount], "%s %s", code, operand1);
                sprintf(ic[(*lineCount)++], "(AD, 01) (C, %d)", currentLocation);
            } else if (strcmp(opcodes[opcodeIndex].code, "LTORG") == 0) {
                for (int i = pools[*poolCount - 1].index; i < *literalCount; i++) {
                    literals[i].location = currentLocation++;
                }
                pools[(*poolCount)++].index = *literalCount;
                sprintf(assembly[*lineCount], "%s", code);
                sprintf(ic[(*lineCount)++], "(AD, 05) (DL, 02)");
            } else if (strcmp(opcodes[opcodeIndex].code, "END") == 0) {
                sprintf(assembly[*lineCount], "%s", code);
                sprintf(ic[(*lineCount)++], "(AD, 02)");
            } else if (strcmp(opcodes[opcodeIndex].code, "ORIGIN") == 0) {
                int originAddress = calculateOperandAddress(operand1, symbols, *symbolCount);
                if (originAddress != -1) {
                    currentLocation = originAddress;
                }
                sprintf(assembly[*lineCount], "%s %s", code, operand1);
                sprintf(ic[(*lineCount)++], "(AD, 03)", currentLocation + 2);
                currentLocation += 2;
            } else if (strcmp(opcodes[opcodeIndex].code, "DS") == 0) {
                sprintf(assembly[*lineCount], "%s %s", code, operand1);
                sprintf(ic[(*lineCount)++], "(S, 0) (DL, 01) (C, %s)", operand1);
                currentLocation += atoi(operand1);
            } else if (operand2[0] == '=') {
                strcpy(literals[*literalCount].value, operand2);
                sprintf(assembly[*lineCount], "%s %s, %s", code, operand1, operand2);
                sprintf(ic[(*lineCount)++], "(IS, %s) (%s) (L, %d)", opcodes[opcodeIndex].machineRep, operand1, *literalCount);
                literals[*literalCount].location = currentLocation++;
                (*literalCount)++;
            } else if (isValidSymbolName(operand2)) {
                int symbolIndex = getSymbolIndex(symbols, operand2, *symbolCount);
                if (symbolIndex == -1) {
                    symbolIndex = addSymbolEntry(symbols, operand2, symbolCount, currentLocation);
                }
                sprintf(assembly[*lineCount], "%s %s, %s", code, operand1, operand2);
                sprintf(ic[(*lineCount)++], "(IS, %s) (%s) (S, %d)", opcodes[opcodeIndex].machineRep, operand1, symbolIndex);
                currentLocation++;
            }
        }
    }

    fclose(file);
}

int main() {
    Opcode opcodes[MAX_MNEMONICS] = {
        {"STOP", "IS", "00", 1}, {"ADD", "IS", "01", 1}, {"SUB", "IS", "02", 1}, {"MULTI", "IS", "03", 1},
        {"MOVER", "IS", "04", 1}, {"MOVEM", "IS", "05", 1}, {"COMP", "IS", "06", 1}, {"BC", "IS", "07", 1},
        {"DIV", "IS", "08", 1}, {"READ", "IS", "09", 1}, {"PRINT", "IS", "10", 1}, {"START", "AD", "01", 0},
        {"END", "AD", "02", 0}, {"ORIGIN", "AD", "03", 0}, {"EQU", "AD", "04", 0}, {"LTORG", "AD", "05", 0},
        {"DS", "DL", "01", 0}, {"DC", "DL", "02", 1}, {"AREG", "RG", "01", 0}, {"BREG", "RG", "02", 0},
        {"CREG", "RG", "03", 0}, {"EQ", "CC", "01", 0}, {"LT", "CC", "02", 0}, {"GT", "CC", "03", 0},
        {"LE", "CC", "04", 0}, {"GE", "CC", "05", 0}, {"NE", "CC", "06", 0}
    };

    LiteralEntry literals[MAX_LITERALS];
    SymbolEntry symbols[MAX_SYMBOLS];
    LiteralPool pools[MAX_POOLS];

    char intermediateCode[MAX_LINES][50];
    char assemblyCode[MAX_LINES][50];
    int lineAddresses[MAX_LINES];

    int literalCount = 0;
    int symbolCount = 0;
    int poolCount = 0;
    int lineCount = 0;

    // Open the output file
    FILE *outputFile = fopen("output.txt", "w");
    if (outputFile == NULL) {
        printf("Error opening file for output!\n");
        return 1;
    }

    // Process the assembly code
    processAssembly(opcodes, literals, symbols, pools, intermediateCode, assemblyCode, lineAddresses, 
                    &literalCount, &symbolCount, &poolCount, &lineCount);

    // Write output to the file
    displayIntermediateCode(intermediateCode, assemblyCode, lineAddresses, lineCount, outputFile);
    displayLiteralTable(literals, literalCount, outputFile);
    displaySymbolTable(symbols, symbolCount, outputFile);
    displayPoolTable(pools, poolCount, outputFile);

    // Close the file
    fclose(outputFile);

    return 0;
}
