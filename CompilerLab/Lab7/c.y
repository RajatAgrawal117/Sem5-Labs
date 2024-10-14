%debug

%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token INT FOR WHILE IF ELSE SWITCH CASE DEFAULT COLON BREAK
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON
%token ASSIGN PLUS MINUS MULT DIV EQ NE GT LT GE LE
%token VARIABLE INTEGER
%token AND OR INCREMENT DECREMENT  

%% 

program:
    statement_list
    ;

statement_list:
    statement_list statement | statement ;

statement: loop_statement | switch_statement | variable_declaration | expression_statement;

loop_statement:
    for_loop
    | while_loop
    ;

for_loop:
    FOR LPAREN expression_statement expression_statement expression RPAREN block
    {
        // Print only after the whole for loop is validated
        printf("Valid 'for' loop detected.\n");
    }
    ;

while_loop:
    WHILE LPAREN expression RPAREN block
    {
        
        printf("Valid 'while' loop detected.\n");
    }
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
    | 
    ;

block:
    LBRACE statement_list RBRACE
    | LBRACE RBRACE
    ;

variable_declaration:
    INT VARIABLE ASSIGN expression SEMICOLON
    {
        
        printf("Valid Integer Declaration detected for variable '%d'.\n", $2);
    }
    ;

expression_statement:
    expression SEMICOLON
    {
       
        printf("Expression statement parsed.\n");
    }
    | SEMICOLON
    ;

expression:
    VARIABLE ASSIGN expression
    {
        
        printf("Assignment expression: %d = ...\n", $1);
    }
    | expression PLUS expression
    | expression MINUS expression
    | expression MULT expression
    | expression DIV expression
    | expression AND expression
    | expression OR expression
    | expression INCREMENT
    | expression DECREMENT
    | VARIABLE
    | INTEGER
    | condition
    ;

condition:
    expression EQ expression
    {
      
        printf("Equality condition detected.\n");
    }
    | expression NE expression
    {
        printf("Not equal condition detected.\n");
    }
    | expression GT expression
    {
        printf("Greater than condition detected.\n");
    }
    | expression LT expression
    {
        printf("Less than condition detected.\n");
    }
    | expression GE expression
    {
        printf("Greater than or equal to condition detected.\n");
    }
    | expression LE expression
    {
        printf("Less than or equal to condition detected.\n");
    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yydebug = 1; // Enable debugging output

    yyparse();
    return 0;
}

