list_a = [1,2,3]
list_b = [3,2,1]
list_a == list_b
print(set(list_a) == set(list_b))


small = set([2,3])
big = set([1,2,3,4])
print(small.issubset(big))