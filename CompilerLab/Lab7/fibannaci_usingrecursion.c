// Fibonacci series using Recursive method

#include<stdio.h>
int fibonacci(int n);




int main()
{
    int n; // variable[to store how many elements to be shown in output]
    printf("Enter the number of elements to be in the series :\n");
    scanf("%d", &n); // user input

    for (int i = 0; i < n; i++)
    {
        printf("%d\n", fibonacci(i));
        // calling fibonacci() fn for each iteration and the return value will be printed

    }

    return 0;
}
int fibonacci(int n)
{
    // 1st condition
    if (n == 0)
    {
        return 0; // return 0 if the condtion will overcome
    }
    // 2nd condition
    else if (n == 1)
    {
        return 1; // returning 1, if the condition mets
    }
    // Now else called the fibonacci() fnct recursively, untill we got the base conditions
    else
    {
        return fibonacci(n-1) + fibonacci(n-2);
        // After calling fib..() function add them like above shown
    
    }
}














// #include<stdio.h>
// int main(){
// int fib(int n);
// int product, i, n, num;
// scanf("%d", &n);
// int fib(int n){
//     if (n == 1 || n == 2):
//         retrun 0;

//     else:
//         retrun fib(n-1)+ fib(n-2);
// }



// return 0;
// }