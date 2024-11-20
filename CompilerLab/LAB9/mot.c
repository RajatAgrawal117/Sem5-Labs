#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define max length for instructions and operands
#define MAX_INSTR 100
#define MAX_OPRND 10

// Structure for symbol table entry
struct SymbolTable {
    char label[20];
    int address;
};

// Structure for intermediate code (Quadruple form)
struct IntermediateCode {
    char op[10];
    char arg1[10];
    char arg2[10];
    char result[10];
};

// Data structures
struct SymbolTable symbolTable[MAX_INSTR];
struct IntermediateCode intermediateCode[MAX_INSTR];
int symTableIndex = 0, interCodeIndex = 0;

// Function to check if a label exists in the symbol table
int searchSymbol(char *label) {
    for (int i = 0; i < symTableIndex; i++) {
        if (strcmp(symbolTable[i].label, label) == 0) {
            return i;
        }
    }
    return -1;
}

// Function to add a label to the symbol table
void addSymbol(char *label, int address) {
    strcpy(symbolTable[symTableIndex].label, label);
    symbolTable[symTableIndex].address = address;
    symTableIndex++;
}

// Function to add intermediate code (quadruple)
void addIntermediateCode(char *op, char *arg1, char *arg2, char *result) {
    strcpy(intermediateCode[interCodeIndex].op, op);
    strcpy(intermediateCode[interCodeIndex].arg1, arg1);
    strcpy(intermediateCode[interCodeIndex].arg2, arg2);
    strcpy(intermediateCode[interCodeIndex].result, result);
    interCodeIndex++;
}

// Function to process assembly instructions
void processAssemblyLine(char *line) {
    char label[20], opcode[10], operand1[10], operand2[10];
    int numTokens = sscanf(line, "%s %s %s %s", label, opcode, operand1, operand2);

    if (numTokens == 2) {
        // No operands, e.g., HALT
        addIntermediateCode(opcode, "-", "-", "-");
    } else if (numTokens == 3) {
        // Single operand, e.g., LOAD A
        addIntermediateCode(opcode, operand1, "-", "-");
    } else if (numTokens == 4) {
        // Two operands, e.g., ADD A, B
        addIntermediateCode(opcode, operand1, operand2, "-");
    }

    // Handle label
    if (strchr(label, ':')) {
        label[strlen(label) - 1] = '\0'; // Remove the colon
        addSymbol(label, interCodeIndex); // Store label in symbol table
    }
}

// Function to print symbol table
void printSymbolTable() {
    printf("Symbol Table:\n");
    printf("Label\tAddress\n");
    for (int i = 0; i < symTableIndex; i++) {
        printf("%s\t%d\n", symbolTable[i].label, symbolTable[i].address);
    }
}

// Function to print intermediate code
void printIntermediateCode() {
    printf("Intermediate Code (Quadruple Form):\n");
    printf("Op\tArg1\tArg2\tResult\n");
    for (int i = 0; i < interCodeIndex; i++) {
        printf("%s\t%s\t%s\t%s\n", intermediateCode[i].op, intermediateCode[i].arg1, intermediateCode[i].arg2, intermediateCode[i].result);
    }
}

int main() {
    FILE *file;
    char line[100];
    
    // Open the assembly file
    file = fopen("input.asm", "r");
    if (!file) {
        printf("Error: Unable to open file.\n");
        return 1;
    }

    // Process each line of the assembly file
    while (fgets(line, sizeof(line), file)) {
        processAssemblyLine(line);
    }

    fclose(file);

    // Print the symbol table and intermediate code
    printSymbolTable();
    printIntermediateCode();

    return 0;
}
