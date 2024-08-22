%{
#include <stdio.h>
#include <string.h>
%}

%%

[0-9]+ {
    int len = yyleng;
    int is_palindrome = 1;
    for (int i = 0; i < len / 2; i++) {
        if (yytext[i] != yytext[len - i - 1]) {
            is_palindrome = 0;
            break;
        }
    }
    if (is_palindrome) {
        printf("%s is a palindrome number\n", yytext);
    } else {
        printf("%s is not a palindrome number\n", yytext);
    }
}

[a-zA-Z]+ {
    int len = yyleng;
    int is_palindrome = 1;
    for (int i = 0; i < len / 2; i++) {
        if (yytext[i] != yytext[len - i - 1]) {
            is_palindrome = 0;
            break;
        }
    }
    if (is_palindrome) {
        printf("%s is a palindrome string\n", yytext);
    } else {
        printf("%s is not a palindrome string\n", yytext);
    }
}

\n {
    // Ignore newline characters
}

. {
    // Ignore any other characters
}

%%

int main(int argc, char **argv) {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}