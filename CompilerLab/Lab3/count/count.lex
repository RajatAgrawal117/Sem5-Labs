%{
#include <stdio.h>

int char_count = 0;
int word_count = 0;
int line_count = 0;
%}

%%
\n              { line_count++; char_count++;}
[ \t]+          { char_count += yyleng;}
[^ \t\n]+       { char_count += yyleng; word_count++;}
.               { char_count++;}
%%

int yywrap() {
    return 1;
}

int main() {
    yylex();
FILE *file = fopen("output.txt","w");
    fprintf(file, "Number of characters: %d\n", char_count);
    fprintf(file, "Number of words: %d\n", word_count);
    fprintf(file, "Number of lines: %d\n", line_count);
    return 0;
}