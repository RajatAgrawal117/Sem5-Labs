%{
#include <stdio.h>
#include <ctype.h>
%}

%%

[a-z]   { printf("%c", toupper(yytext[0])); }
[A-Z]   { printf("%s", yytext); }
.       { printf("%s", yytext); }

%%

int main()
{
    printf("Enter any string: ");
    yylex();
    return 0;
}

int yywrap()
{
    return 1;
}
