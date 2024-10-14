%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token SWITCH CASE DEFAULT COLON BREAK SEMICOLON VARIABLE INTEGER

%%

program:
    statement_list
    ;

statement_list:
    statement_list statement
    | statement
    ;

statement:
    switch_statement
    | variable_declaration
    | expression_statement
    ;

switch_statement:
    SWITCH LPAREN expression RPAREN LBRACE case_list default_clause_opt RBRACE
    {
        printf("Valid 'switch' statement detected.\n");
    }
    ;

case_list:
    case_list case_clause
    | case_clause
    ;

case_clause:
    CASE expression COLON statement_list BREAK SEMICOLON
    {
        printf("Valid 'case' clause detected.\n");
    }
    ;

default_clause_opt:
    DEFAULT COLON statement_list BREAK SEMICOLON
    {
        printf("Valid 'default' clause detected.\n");
    }
    | /* empty */  // The default clause is optional
    ;

variable_declaration:
    VARIABLE ASSIGN expression SEMICOLON
    {
        printf("Valid variable declaration.\n");
    }
    ;

expression_statement:
    expression SEMICOLON
    {
        printf("Expression statement detected.\n");
    }
    ;

expression:
    VARIABLE
    | INTEGER
    | expression PLUS expression
    | expression MINUS expression
    | expression MULT expression
    | expression DIV expression
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}
