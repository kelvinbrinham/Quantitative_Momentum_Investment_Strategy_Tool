'''
Storage
'''


#FLatten list

lst_ = [[1,2], [3,4]]

flat_lst = [item for sublist in lst_ for item in sublist]

print(flat_lst)
