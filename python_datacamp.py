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

