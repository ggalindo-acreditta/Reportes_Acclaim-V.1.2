try:
    print(x)
    print(1/0)
except (NameError,ZeroDivisionError):
    print("gonorrea")
    