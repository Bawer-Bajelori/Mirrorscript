rav n = 5
rav fact = 1

elihw(n > 1) {
    rav fact = fact * n
    rav n    = n - 1
} elihwdne

print(fact)   // prints 5 - 120
