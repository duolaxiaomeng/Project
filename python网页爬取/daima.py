n, k = map(int, input().split())
ans = 1
h = 10 ** k
nums = list(map(int, input().split()))
for a in nums:
    if h  <= ans*a:
        ans = 1
        continue
    ans *= a
print(ans)