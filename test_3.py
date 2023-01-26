'''
test 3
'''
import pandas as pd

my_columns = ['First Name', 'Last Name', 'Age']
df = pd.DataFrame(columns=my_columns)


kel = ['Kelvin', 'Brinham', 23]
rob = ['Rob', 'Brinham', 59]
Rache = ['Rachel', 'Brinham', 60]

people_lst = [kel, rob, Rache]

df2 = pd.concat(df, people_lst)



print(df2)
