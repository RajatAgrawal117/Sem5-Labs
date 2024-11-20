#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_MNEMONICS 29
#define MAX_LITERALS 10
#define MAX_SYMBOLS 10
#define MAX_POOLS 10
#define MAX_CODE_LINES 100

// Structure to store mnemonic details
struct Mnemonic {
    char mnemonic[10];
    char class[3];
    char machineCode[10];
    int length;
};

// Structure to store literal details
struct Literal {
    char literal[10];
    int address;
};

// Structure to store symbol details
struct Symbol {
    char symbol[10];
    int address;
};

// Structure to store pool table details
struct Pool {
    int startIndex;
};


// Function to print intermediate code with proper alignment
void printIntermediateCode(char ic[MAX_CODE_LINES][50], char assemblyCode[MAX_CODE_LINES][50], int lc[MAX_CODE_LINES], int icCount) {
    printf("\nIntermediate Code:\n");
    printf("%-25s %-30s %-20s\n", "Assembly Code", "Intermediate Code", "Location Counter");
    printf("%-25s %-30s %-20s\n", "---------------", "-------------------", "----------------");
    
    for (int i = 0; i < icCount; i++) {
        printf("%-25s %-30s %-20d\n", assemblyCode[i], ic[i], lc[i]);
    }
}

// Function to print the literal table
void printLiteralTable(struct Literal literals[], int literalCount) {
    printf("\nLiteral Table:\n");
    printf("Index\tLiteral\tAddress\n");
    for (int i = 0; i < literalCount; i++) {
        printf("%d\t%s\t%d\n", i, literals[i].literal, literals[i].address);
    }
}

// Function to print the symbol table
void printSymbolTable(struct Symbol symbols[], int symbolCount) {
    printf("\nSymbol Table:\n");
    printf("Index\tSymbol\tAddress\n");
    for (int i = 0; i < symbolCount; i++) {
        printf("%d\t%s\t%d\n", i, symbols[i].symbol, symbols[i].address);
    }
}

// Function to print the pool table
void printPoolTable(struct Pool pools[], int poolCount) {
    printf("\nPool Table:\n");
    printf("Pool No.\tLiteral Start Index\n");
    for (int i = 0; i < poolCount; i++) {
        printf("%d\t\t%d\n", i, pools[i].startIndex);
    }
}

// Function to find mnemonic in the table
int findMnemonic(struct Mnemonic mnemonics[], char *mnemonic, int count) {
    for (int i = 0; i < count; i++) {
        if (strcmp(mnemonics[i].mnemonic, mnemonic) == 0) {
            return i;
        }
    }
    return -1;
}

// Function to find symbol in the symbol table
int findSymbol(struct Symbol symbols[], char *symbol, int symbolCount) {
    for (int i = 0; i < symbolCount; i++) {
        if (strcmp(symbols[i].symbol, symbol) == 0) {
            return i;
        }
    }
    return -1;
}

// Function to add a new symbol to the symbol table
int addSymbol(struct Symbol symbols[], char *symbol, int *symbolCount, int currentAddress) {
    strcpy(symbols[*symbolCount].symbol, symbol);
    symbols[*symbolCount].address = currentAddress;
    (*symbolCount)++;
    return *symbolCount - 1;  // Return the index of the newly added symbol
}

// Function to check if a string is a valid symbol (not an integer)
int isValidSymbol(char *str) {
    return !isdigit(str[0]); // Valid if it does not start with a digit
}

// Main function to process the assembly code
int main() {
    struct Mnemonic mnemonics[MAX_MNEMONICS] = {
        {"STOP",   "IS", "00",     1},
        {"ADD",    "IS", "01",     1},
        {"SUB",    "IS", "02",     1},
        {"MULTI",  "IS", "03",     1},
        {"MOVER",  "IS", "04",     1},
        {"MOVEM",  "IS", "05",     1},
        {"COMP",   "IS", "06",     1},
        {"BC",     "IS", "07",     1},
        {"DIV",    "IS", "08",     1},
        {"READ",   "IS", "09",     1},
        {"PRINT",  "IS", "10",     1},
        {"START",  "AD", "01",     0},
        {"END",    "AD", "02",     0},
        {"ORIGIN", "AD", "03",     0},
        {"EQU",    "AD", "04",     0},
        {"LTORG",  "AD", "05",     0},
        {"DS",     "DL", "01",     0},
        {"DC",     "DL", "02",     1},
        {"A",      "RG", "01",     0},
        {"B",      "RG", "02",     0},
        {"C",      "RG", "03",     0},
        {"EQ",     "CC", "01",     0},
        {"LT",     "CC", "02",     0},
        {"GT",     "CC", "03",     0},
        {"LE",     "CC", "04",     0},
        {"GE",     "CC", "05",     0},
        {"NE",     "CC", "06",     0}
    };

    struct Literal literals[MAX_LITERALS];
    struct Symbol symbols[MAX_SYMBOLS];
    struct Pool pools[MAX_POOLS];
    int literalCount = 0, symbolCount = 0, poolCount = 0, currentAddress = 0, icCount = 0;
    char intermediateCode[MAX_CODE_LINES][50];
    char assemblyCode[MAX_CODE_LINES][50];
    int lc[MAX_CODE_LINES]; // Location counter for intermediate code
    char line[100], mnemonic[10], operand1[10], operand2[10];

    FILE *file = fopen("input.txt", "r");

    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Initialize first pool starting from literal index 0
    pools[poolCount++].startIndex = literalCount;

    while (fgets(line, sizeof(line), file)) {
        sscanf(line, "%s %s %s", mnemonic, operand1, operand2);

        int mIndex = findMnemonic(mnemonics, mnemonic, MAX_MNEMONICS);

        if (mIndex != -1) {
            // Store the current location counter
            lc[icCount] = currentAddress;

            // Handle START
            if (strcmp(mnemonics[mIndex].mnemonic, "START") == 0) {
                currentAddress = atoi(operand1);  // Convert operand1 to integer
                sprintf(assemblyCode[icCount], "%s %s", mnemonic, operand1);
                sprintf(intermediateCode[icCount++], "(AD, %s) (C, %d)", mnemonics[mIndex].machineCode, currentAddress);
            }
            // Handle LTORG
            else if (strcmp(mnemonics[mIndex].mnemonic, "LTORG") == 0) {
                for (int i = pools[poolCount - 1].startIndex; i < literalCount; i++) {
                    literals[i].address = currentAddress++;
                }
                pools[poolCount++].startIndex = literalCount;  // New pool starts
                sprintf(assemblyCode[icCount], "%s", mnemonic);
                sprintf(intermediateCode[icCount++], "(AD, %s)", mnemonics[mIndex].machineCode);
            }
            // Handle END
            else if (strcmp(mnemonics[mIndex].mnemonic, "END") == 0) {
                sprintf(assemblyCode[icCount], "%s", mnemonic);
                sprintf(intermediateCode[icCount++], "(AD, %s)", mnemonics[mIndex].machineCode);
            }
            // Handle instructions with literals
            else if (operand2[0] == '=') {
                // Assign the current address to the literal
                strcpy(literals[literalCount].literal, operand2);
                literals[literalCount].address = currentAddress;  // Set address of the literal
                sprintf(assemblyCode[icCount], "%s %s", mnemonic, operand2);
                sprintf(intermediateCode[icCount++], "(IS, %s) (RG, 01) (L, %d)", mnemonics[mIndex].machineCode, literalCount);
                literalCount++; // Increment the count of literals
                currentAddress++; // Move to next address for the next instruction
            }
            // Handle instructions with registers and symbols (variables)
            else if (isValidSymbol(operand2)) {
                int symbolIndex = findSymbol(symbols, operand2, symbolCount);
                if (symbolIndex == -1) {
                    symbolIndex = addSymbol(symbols, operand2, &symbolCount, currentAddress);
                }
                sprintf(assemblyCode[icCount], "%s %s", mnemonic, operand2);
                sprintf(intermediateCode[icCount++], "(IS, %s) (RG, 01) (S, %d)", mnemonics[mIndex].machineCode, symbolIndex);
                currentAddress++; // Move to next address for the next instruction
            }
        }
    }

    fclose(file);


    printIntermediateCode(intermediateCode, assemblyCode, lc, icCount);
    printLiteralTable(literals, literalCount);
    printSymbolTable(symbols, symbolCount);
    printPoolTable(pools, poolCount);

    return 0;
}