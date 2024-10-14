int n; // variable[to store how many elements to be shown in output]
    printf("Enter the number of elements to be in the series :\n");
    scanf("%d", &n); // user input

    for (int i = 0; i < n; i++)
    {
        printf("%d\n", fibonacci(i));
        // calling fibonacci() fn for each iteration and the return value will be printed

    }
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