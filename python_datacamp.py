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
