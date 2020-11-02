def permutations(list, k):
    if k <= 0:
        yield []
    else:
        n = len(list)
        # if n == k:
        for i in range(n-k+1):
            l = list[i]
            for perm in permutations(list[i+1:], k-1):
                perm.append(l)
                yield perm