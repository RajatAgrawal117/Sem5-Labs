%{
#include "y.tab.h"
#include <stdio.h>
%}

%%

"int"           { return INT; }
"for"           { return FOR; }
"while"         { return WHILE; }
"if"            { return IF; }
"else"          { return ELSE; }
"switch"        { return SWITCH; }
"case"          { return CASE; }
"default"       { return DEFAULT; }
"break"         { return BREAK; }


"("             { return LPAREN; }
")"             { return RPAREN; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
";"             { return SEMICOLON; }
":"             { return COLON; }
"="             { return ASSIGN; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULT; }
"/"             { return DIV; }
"=="            { return EQ; }
"!="            { return NE; }
">"             { return GT; }
"<"             { return LT; }
">="            { return GE; }
"<="            { return LE; }
"&&"            { return AND; }
"||"            { return OR; }
"++"            { return INCREMENT; }
"--"            { return DECREMENT; }

[a-zA-Z_][a-zA-Z0-9_]*  {
    return VARIABLE;
}

[0-9]+          { yylval = atoi(yytext); return INTEGER; }

[ \t\n\r]+      { }

.               { printf("Unknown character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}

