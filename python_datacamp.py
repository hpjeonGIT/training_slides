# Lambda function
say_word = (lambda word0, n: word0*n)
result = say_word('hello ',5)
print(result)

# map and Lambda function
fruits = ["apple", "banana", "orange"]
say_fruits = map(lambda snack:snack+ '!!!',fruits)
say_fruits_list = list(say_fruits)
print(say_fruits_list)

# Handling error
def sq(x):
  try:
    return x*x
  except TypeError:
    print('x is not an int nor float')
# or use `raise ValueError('comment')`

# Iterator
fruits = ["apple", "banana", "orange"]
iter_fruits = iter(fruits)
print(next(iter_fruits))
print(next(iter_fruits))

manynumber = iter(range(10**100)) # Doesn't store statically. Saves memory

# Reading a large file chunk by chunk (saves memory)
for chunk in pd.read_csv('my.csv',chunksize=10):
  for word in chunk['item']:
    # do somehting here
    
# List comprehension
a_list = [i for i in range(10)]
b_list = [1 if x >5 else -1 for x in a_list]    

# Generator
## dynamic version of comprehension. Good for very large data or streaming
## [] => ()
a_list = (i for i in range(10))
print(next(a_list))

# importing file data
## flat file
with open('my.txt') as f:
  print(f.readline())
  print(f.readline())
  
## using numpy
import numpy as np
data = np.loadtxt('my.csv',delimter=',', skiprows=1,usecols=[0,2])

## pandas
import pandas as pd
data = pd.read_csv('my.csv', nrows=10, header=None)
darray = np.array(data.values)

## pickle
import pickle
with open('my.pkl','rb') as f:
  a = pickle.load(f)
  
## Excel using pandas
import pandas as pd
xls = pd.ExcelFile('my.xlsx')
print(xls.sheet_names)
df1 = xls.parse('2019') # dump 2019 sheet into dataframe

## SAS
from sas7bdat import SAS7BDAT
with SAS7BDAT('ex.sas7bdat') as f:
  df = f.to_data_frame()

## STATA  
import pandas as pd
df = pd.read_stata('my.dta')

## HDF5
import numpy as np
import hdf5
data = h5py.File('my.hdf5','r')
for key in data.keys():
  print(key)
  
## MATLAB
import scipy.io
data = scipy.io.loadmat('my.mat')
print(mat.keys())

## SQL
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('sqlite:///my.sqlite')
con = engine.connect()
rs = con.execute('SELECT * FROM Address')
df = pd.DataFRame(rs.fetchall())
con.close()
###
with engine.connect() as con:
  rs = con.execute("SELECT * FROM Address")
  df = pd.DataFrame(rs.fetchmany(10))
  df.columns = rs.keys()
###  
engine = create_engine('sqlite:///my.sqlite')
df = pd.read_sql_query('SELECT * FROM Address',engine)

## Flat/Excel file from WWW
url = 'https://s3.amazonaws.com/mydata/my.csv'
df = pd.read_csv(url,sep=';')
print(df.head())
url = 'https://s3.amazonaws.com/mydata/my.xls'
xls = pd.read_excel(url,sep=';')

## JSON
with open('my.json') as f:
  jdata = json.load(f)
for key in jdata.keys():
  print(key+':',jdata[key])
print(xls.keys())
