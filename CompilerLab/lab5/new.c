#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_PRODUCTIONS 10
#define MAX_SYMBOLS 100

void findFirst(char, int, int);
void followFirst(char, int, int);
void follow(char c);

int count, n = 0;
char calc_first[MAX_PRODUCTIONS][MAX_SYMBOLS];
char calc_follow[MAX_PRODUCTIONS][MAX_SYMBOLS];
int m = 0;
char production[MAX_PRODUCTIONS][MAX_SYMBOLS], first[MAX_SYMBOLS];
char f[MAX_SYMBOLS];
int k;
char ck;
int e;

int main() {
    int i, j;
    char c, ch;

    printf("How many productions? : ");
    scanf("%d", &count);

    printf("\nEnter %d productions in form A=B where A and B are grammar symbols:\n\n", count);
    for (i = 0; i < count; i++) {
        scanf("%s", production[i]);
    }

    // Initialize calc_first array
    for (i = 0; i < count; i++) {
        for (j = 0; j < MAX_SYMBOLS; j++) {
            calc_first[i][j] = '!';
        }
    }

    // Find FIRST sets for each production
    for (i = 0; i < count; i++) {
        c = production[i][0];
        findFirst(c, 0, 0);
        printf("\nFirst(%c) = { ", c);
        for (j = 0; j < n; j++) {
            printf("%c ", first[j]);
        }
        printf("}\n");
        n = 0;
    }

    // Initialize calc_follow array
    for (i = 0; i < count; i++) {
        for (j = 0; j < MAX_SYMBOLS; j++) {
            calc_follow[i][j] = '!';
        }
    }

    // Find FOLLOW sets for each non-terminal
    for (i = 0; i < count; i++) {
        ck = production[i][0];
        follow(ck);
        printf("Follow(%c) = { ", ck);
        for (j = 0; j < m; j++) {
            printf("%c ", f[j]);
        }
        printf("}\n");
        m = 0;
    }

    return 0;
}

// Function to find FIRST set of a non-terminal
void findFirst(char c, int q1, int q2) {
    int j;

    if (!isupper(c)) {  // Terminal
        first[n++] = c;
        return;
    }

    for (j = 0; j < count; j++) {
        if (production[j][0] == c) {
            if (production[j][2] == '#') {  // Epsilon production
                first[n++] = '#';
            } else if (islower(production[j][2])) {  // Terminal in RHS
                first[n++] = production[j][2];
            } else {  // Non-terminal in RHS
                findFirst(production[j][2], q1, q2);
            }
        }
    }
}

// Function to find FOLLOW set of a non-terminal
void follow(char c) {
    int i, j;

    if (production[0][0] == c) {
        f[m++] = '$';  // Start symbol
    }

    for (i = 0; i < count; i++) {
        for (j = 2; j < strlen(production[i]); j++) {
            if (production[i][j] == c) {
                if (production[i][j + 1] != '\0') {
                    followFirst(production[i][j + 1], i, (j + 2));
                }
                if (production[i][j + 1] == '\0' && c != production[i][0]) {
                    follow(production[i][0]);
                }
            }
        }
    }
}

// Helper function for FOLLOW to handle non-terminals
void followFirst(char c, int c1, int c2) {
    if (!isupper(c)) {
        f[m++] = c;
    } else {
        int i = 0, j = 1;
        for (i = 0; i < count; i++) {
            if (calc_first[i][0] == c) {
                break;
            }
        }
        while (calc_first[i][j] != '!') {
            if (calc_first[i][j] != '#') {
                f[m++] = calc_first[i][j];
            } else {
                follow(production[c1][0]);
            }
            j++;
        }
    }
}
