'''
test 2
'''


lst1 = [1, 2, 3]
lst2 = [10, 20, 30]

lst3 = [lst1[i] * lst2[i] for i in range(len(lst1))]
print(lst3)
