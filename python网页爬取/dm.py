v = []
n = int(input())
for i in range(9, 1, -1):
    while n % i == 0:
        v.append(i)
        n = n // i

if n >= 10:
    print("There is no such number!")
else:
    v.sort()
    for x in v:
        print(x, end='')