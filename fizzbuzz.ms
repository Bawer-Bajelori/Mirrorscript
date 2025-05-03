rav n = 1

# Loop from 1 to 100
elihw(n <= 100)
    # ——————— compute n mod 3 ———————
    rav tmp3 = n
    elihw(tmp3 >= 3)
        rav tmp3 = tmp3 + -3
    elihwdne

    # ——————— compute n mod 5 ———————
    rav tmp5 = n
    elihw(tmp5 >= 5)
        rav tmp5 = tmp5 + -5
    elihwdne

    # 1 FizzBuzz if divisible by both 3 and 5
    fi(tmp3 == 0)
        fi(tmp5 == 0)
            print("FizzBuzz")
        fidne
    fidne

    # 2 Fizz if divisible by 3 only
    fi(tmp3 == 0)
        print("Fizz")
    fidne

    # 3 Buzz if divisible by 5 only
    fi(tmp5 == 0)
        print("Buzz")
    fidne

    # 4 Otherwise print the number
    fi(tmp3 != 0)
        fi(tmp5 != 0)
            print(n)
        fidne
    fidne

    # increment n
    rav n = n + 1
elihwdne
