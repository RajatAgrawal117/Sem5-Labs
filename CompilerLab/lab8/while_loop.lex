%{
#include "while_loop.tab.h"
#include <stdlib.h>
#include <stdio.h>
%}

%%

"while"         { printf("Token: WHILE\n"); return WHILE; }
"if"            { printf("Token: IF\n"); return IF; }
"else"          { printf("Token: ELSE\n"); return ELSE; }
"switch"        { printf("Token: SWITCH\n"); return SWITCH; }
"case"          { printf("Token: CASE\n"); return CASE; }
"default"       { printf("Token: DEFAULT\n"); return DEFAULT; }
"break"         { printf("Token: BREAK\n"); return BREAK; }

"("             { printf("Token: LPAREN\n"); return LPAREN; }
")"             { printf("Token: RPAREN\n"); return RPAREN; }
"{"             { printf("Token: LBRACE\n"); return LBRACE; }
"}"             { printf("Token: RBRACE\n"); return RBRACE; }
";"             { printf("Token: SEMICOLON\n"); return SEMICOLON; }
":"             { printf("Token: COLON\n"); return COLON; }

[0-9]+          { yylval = atoi(yytext); printf("Token: NUMBER (%d)\n", yylval); return NUMBER; }

[ \t\n]+        { /* ignore whitespace */ }

.               { printf("Unrecognized character: '%s'\n", yytext); }

%%

int yywrap() {
    return 1;
}
