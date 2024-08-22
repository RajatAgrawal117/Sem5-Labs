#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STEPS 100

// Struct to store parsing steps
typedef struct {
    char non_terminal[10];
    char action[20];
    char symbol[5];
} ParsingStep;

ParsingStep steps[MAX_STEPS];  // Table for parsing steps
int step_count = 0;            // Number of steps recorded

char *input;
int pos = 0;

void add_step(const char *non_terminal, const char *action, char symbol) {
    if (step_count < MAX_STEPS) {
        strcpy(steps[step_count].non_terminal, non_terminal);
        strcpy(steps[step_count].action, action);
        snprintf(steps[step_count].symbol, sizeof(steps[step_count].symbol), "%c", symbol);
        step_count++;
    }
}

void add_step_str(const char *non_terminal, const char *action, const char *symbol) {
    if (step_count < MAX_STEPS) {
        strcpy(steps[step_count].non_terminal, non_terminal);
        strcpy(steps[step_count].action, action);
        strncpy(steps[step_count].symbol, symbol, sizeof(steps[step_count].symbol));
        step_count++;
    }
}

void match(char expected) {
    if (input[pos] == expected) {
        add_step("Match", "Matched", expected);
        pos++;
    } else {
        add_step("Error", "Expected", expected);
        exit(1);
    }
}

void E();  // Forward declarations
void E1();
void T();
void T1();
void F();
void F1();
void P();

// Parse the grammar for E -> T E'
void E() {
    add_step("E", "Enter", input[pos]);
    T();
    E1();
}

// Parse the grammar for E' -> + T E' | - T E' | ε
void E1() {
    add_step("E'", "Enter", input[pos]);
    if (input[pos] == '+') {
        match('+');
        T();
        E1();
    } else if (input[pos] == '-') {
        match('-');
        T();
        E1();
    }
    // ε production
}

// Parse the grammar for T -> F T'
void T() {
    add_step("T", "Enter", input[pos]);
    F();
    T1();
}

// Parse the grammar for T' -> * F T' | / F T' | ε
void T1() {
    add_step("T'", "Enter", input[pos]);
    if (input[pos] == '*') {
        match('*');
        F();
        T1();
    } else if (input[pos] == '/') {
        match('/');
        F();
        T1();
    }
    // ε production
}

// Parse the grammar for F -> P F'
void F() {
    add_step("F", "Enter", input[pos]);
    P();
    F1();
}

// Parse the grammar for F' -> ^ F | ε
void F1() {
    add_step("F'", "Enter", input[pos]);
    if (input[pos] == '^') {
        match('^');
        F();
    }
    // ε production
}

// Parse the grammar for P -> ( E ) | id
void P() {
    add_step("P", "Enter", input[pos]);
    if (input[pos] == '(') {
        match('(');
        E();
        match(')');
    } else if (input[pos] == 'i' && input[pos + 1] == 'd') {
        add_step_str("P", "Matched", "id");
        pos += 2;  // Skip 'id'
    } else {
        add_step("Error", "Expected ( or id", input[pos]);
        exit(1);
    }
}

// Function to print the parsing table
void print_parsing_table() {
    printf("\nParsing Table:\n");
    printf("%-10s | %-20s | %-5s\n", "Non-Term", "Action", "Symbol");
    printf("--------------------------------------\n");
    for (int i = 0; i < step_count; i++) {
        printf("%-10s | %-20s | %-5s\n", steps[i].non_terminal, steps[i].action, steps[i].symbol);
    }
}

int main() {
    char buffer[256];
    printf("Enter the input string: ");
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strcspn(buffer, "\n")] = '\0';  
    input = buffer;

    printf("Starting parsing...\n");
    E();
    if (input[pos] == '\0') {
        add_step_str("Success", "Parsing", "Complete");  
        print_parsing_table();
        printf("Parsing successful!\n");
    } else {
        add_step("Error", "Unexpected input at end", input[pos]);
        print_parsing_table();
        printf("Error: Unexpected input at end of string\n");
    }

    return 0;
}
