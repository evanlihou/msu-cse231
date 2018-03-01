x = 1
while x <= 100:
    p = ""
    if x % 3 == 0:
        p += "Fizz"
    if x % 5 == 0:
        p += "Buzz."
    print(x, p)
    x += 1