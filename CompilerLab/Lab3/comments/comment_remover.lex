%{
#include<stdio.h>
int sl = 0;     // Counter for single-line comments
int ml = 0;     // Counter for multi-line comments
FILE *commentFile;
%}
%%
"/*"[a-zA-Z0-9' '\t\n]+"*/"  { 
    ml++; 
    fprintf(commentFile, "Multiline Comment %d: %s\n", ml, yytext);
}
"//".* { 
    sl++; 
    fprintf(commentFile, "Single-line Comment %d: %s\n", sl, yytext);
}
.|\n { 
    fputc(yytext[0], yyout); 
}
%%
int main() {
    // Open input, output, and comment files
    yyin = fopen("test1.c", "r");
    yyout = fopen("input.c", "w");
    commentFile = fopen("comments.txt", "w");

    if(yyin == NULL || yyout == NULL || commentFile == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    yylex();  // Run lexical analyzer

    // Close all opened files
    fclose(yyin);
    fclose(yyout);
    fclose(commentFile);

    // Print the number of comments found
    printf("\nNumber of single line comments: %d\n", sl);
    printf("Number of multiline comments: %d\n", ml);

    return 0;
}
