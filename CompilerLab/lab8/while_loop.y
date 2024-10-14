%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex(void);
#define YYDEBUG 1  // Enable debugging
%}

/* Declare tokens */
%token NUMBER IF ELSE SWITCH CASE DEFAULT BREAK WHILE
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON COLON

%%

program:
    statements
    ;

statements:
    statements statement
    | statement
    ;

statement:
    IF LPAREN condition RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE {
        printf("Parsed if-else statement with condition: %d\n", $3);
    }
    | IF LPAREN condition RPAREN LBRACE statements RBRACE {
        printf("Parsed if statement with condition: %d\n", $3);
    }
    | WHILE LPAREN condition RPAREN LBRACE statements RBRACE {
        printf("Parsed while loop with condition: %d\n", $3);
    }
    ;
    | LBRACE statements RBRACE {
        printf("Parsed a block of statements.\n");
    }
    | NUMBER SEMICOLON {
        printf("Parsed number: %d\n", $1);
    }
    | SWITCH LPAREN condition RPAREN LBRACE switch_body RBRACE {
        printf("Parsed switch statement with condition: %d\n", $3);
    }
    ;

switch_body:
    switch_case_list DEFAULT COLON statements {
        printf("Parsed default case.\n");
    }
    | switch_case_list
    ;

switch_case_list:
    switch_case_list switch_case
    | switch_case
    ;

switch_case:
    CASE NUMBER COLON statements {
        printf("Parsed case %d:\n", $2);
    }
    ;

condition:
    NUMBER {
        printf("Parsed condition: %d\n", $1);
    }
    ;

%%

// Error handling function
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    extern int yydebug;
    yydebug = 1;  // Turn on parser debugging
    printf("Starting parser...\n");
    int result = yyparse();
    printf("Parsing complete with result: %d\n", result);
    return result;
}
