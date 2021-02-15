import sys

salida = sys.stdout
foo = sys.stdin.readline()
print (foo)


sys.stdout = open("Salida.txt","w")
print(foo)

for i in range(5):
    print(i)
    salida.write(str(i+2))
