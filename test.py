'''
test
'''

lst1 = [1,2,3]

lst2 = [9,8,4]

lst3 = [lst1[i] * lst2[i] for i in range(len(lst1))]

print(lst3)
