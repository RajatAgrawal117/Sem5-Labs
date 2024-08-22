// make a c program that checks if a grammar or production rules are valid and accepted by  RDP (Recursive Descent Parser) and use recursive functions, and print out the step by step parsing in terminal

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *input;
int pos = 0;

void match(char expected)
{
    if (input[pos] == expected)
    {
        printf("Matched %c\n", expected);
        pos++;
    }
    else
    {
        printf("Error: Expected %c but found %c\n", expected, input[pos]);
        exit(1);
    }
}

void E(); // Forward declarations
void E1();
void T();
void T1();
void F();
void F1();
void P();

// Parse the grammar for E -> T E'
void E()
{
    printf("Parsing E\n");
    T();
    E1();
}

// Parse the grammar for E' -> + T E' | - T E' | ε
void E1()
{
    printf("Parsing E'\n");
    if (input[pos] == '+')
    {
        match('+');
        T();
        E1();
    }
    else if (input[pos] == '-')
    {
        match('-');
        T();
        E1();
    }
    // ε production (do nothing)
}

// Parse the grammar for T -> F T'
void T()
{
    printf("Parsing T\n");
    F();
    T1();
}

// Parse the grammar for T' -> * F T' | / F T' | ε
void T1()
{
    printf("Parsing T'\n");
    if (input[pos] == '*')
    {
        match('*');
        F();
        T1();
    }
    else if (input[pos] == '/')
    {
        match('/');
        F();
        T1();
    }
    // ε production (do nothing)
}

// Parse the grammar for F -> P F'
void F()
{
    printf("Parsing F\n");
    P();
    F1();
}

// Parse the grammar for F' -> ^ F | ε
void F1()
{
    printf("Parsing F'\n");
    if (input[pos] == '^')
    {
        match('^');
        F();
    }
    // ε production (do nothing)
}

// Parse the grammar for P -> ( E ) | id
void P()
{
    printf("Parsing P\n");
    if (input[pos] == '(')
    {
        match('(');
        E();
        match(')');
    }
    else if (input[pos] == 'i' && input[pos + 1] == 'd')
    {
        printf("Matched id\n");
        pos += 2; // Skip 'id'
    }
    else
    {
        printf("Error: Expected ( or id but found %c\n", input[pos]);
        exit(1);
    }
}

int main()
{
    // Input example: (id+id*id)^id
    char buffer[256];
    printf("Enter the input string: ");
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strcspn(buffer, "\n")] = '\0'; // Remove trailing newline
    input = buffer;

    printf("Starting parsing...\n");
    E();
    if (input[pos] == '\0')
    {
        printf("Parsing successful!\n");
    }
    else
    {
        printf("Error: Unexpected input at end of string\n");
    }

    return 0;
}