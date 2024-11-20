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

void displayIntermediateCode(char ic[MAX_LINES][50], char assembly[MAX_LINES][50], int addresses[MAX_LINES], int totalLines, FILE *outputFile) {
    fprintf(outputFile, "\n+----------------------+------------+--------------------------------+\n");
    fprintf(outputFile, "| %-20s | %-10s | %-30s |\n", "SRC", "LC", "IC");
    fprintf(outputFile, "+----------------------+------------+--------------------------------+\n");

    for (int i = 0; i < totalLines; i++) {
        fprintf(outputFile, "| %-20s | %-10d | %-30s |\n", assembly[i], addresses[i], ic[i]);
    }

    fprintf(outputFile, "+----------------------+------------+--------------------------------+\n");
}

void displayLiteralTable(LiteralEntry literals[], int literalCount, FILE *outputFile) {
    fprintf(outputFile, "\n+-------+-----------------+------------+\n");
    fprintf(outputFile, "| %-5s | %-15s | %-10s |\n", "Index", "Literal", "Address");
    fprintf(outputFile, "+-------+-----------------+------------+\n");

    for (int i = 0; i < literalCount; i++) {
        fprintf(outputFile, "| %-5d | %-15s | %-10d |\n", i, literals[i].value, literals[i].location);
    }

    fprintf(outputFile, "+-------+-----------------+------------+\n");
}

void displaySymbolTable(SymbolEntry symbols[], int symbolCount, FILE *outputFile) {
    fprintf(outputFile, "\n+-------+-----------------+------------+\n");
    fprintf(outputFile, "| %-5s | %-15s | %-10s |\n", "Index", "Symbol", "Address");
    fprintf(outputFile, "+-------+-----------------+------------+\n");

    for (int i = 0; i < symbolCount; i++) {
        fprintf(outputFile, "| %-5d | %-15s | %-10d |\n", i, symbols[i].name, symbols[i].location);
    }

    fprintf(outputFile, "+-------+-----------------+------------+\n");
}

void displayPoolTable(LiteralPool pools[], int poolCount, FILE *outputFile) {
    fprintf(outputFile, "\n+----------+---------------------+\n");
    fprintf(outputFile, "| %-5s | %-15s |\n", "Pool No.", "Literal Start Index");
    fprintf(outputFile, "+----------+---------------------+\n");

    for (int i = 0; i < poolCount; i++) {
        fprintf(outputFile, "| %-8d | %-19d |\n", i, pools[i].index);
    }

    fprintf(outputFile, "+----------+---------------------+\n");
}

// Rest of the code remains the same...

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

    // Open separate files for each table
    FILE *icFile = fopen("intermediate_code.txt", "w");
    FILE *literalFile = fopen("literal_table.txt", "w");
    FILE *symbolFile = fopen("symbol_table.txt", "w");
    FILE *poolFile = fopen("pool_table.txt", "w");

    if (!icFile || !literalFile || !symbolFile || !poolFile) {
        printf("Error opening one or more output files!\n");
        return 1;
    }

    // Call each function and pass the corresponding file pointer
    displayIntermediateCode(intermediateCode, assemblyCode, lineAddresses, lineCount, icFile);
    displayLiteralTable(literals, literalCount, literalFile);
    displaySymbolTable(symbols, symbolCount, symbolFile);
    displayPoolTable(pools, poolCount, poolFile);

    // Close the files
    fclose(icFile);
    fclose(literalFile);
    fclose(symbolFile);
    fclose(poolFile);

    printf("Tables successfully written to separate files.\n");

    return 0;
}
