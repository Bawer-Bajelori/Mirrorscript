rav n = 1;

// this will loop from 1 to 100
elihw(n <= 100) {
    // this is for 3
    rav tmp3 = n;
    elihw(tmp3 >= 3) {
        tmp3 = tmp3 + -3;
    }

    // this is for 5
    rav tmp5 = n;
    elihw(tmp5 >= 5) {
        tmp5 = tmp5 + -5;
    }

    // 1) FizzBuzz if divisible by both 3 and 5
    fi(tmp3 == 0) {
        fi(tmp5 == 0) {
            print("FizzBuzz");
        }
    }

    // 2) Fizz if divisible by 3 only
    fi(tmp3 == 0) {
        print("Fizz");
    }

    // 3) Buzz if divisible by 5 only
    fi(tmp5 == 0) {
        print("Buzz");
    }

    // 4) Otherwise print the number
    fi(tmp3 != 0) {
        fi(tmp5 != 0) {
            print(n);
        }
    }

    // this will increment n
    n = n + 1;
}
