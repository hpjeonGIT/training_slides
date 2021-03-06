# Python
- Preparation of testing data. Random data of product id and property x/y
```python
import numpy
import time
import random
import pandas as pd
N = 100000

x = [random.random() for i in range(N)]
y = [random.random() for i in range(N)]
indx = [i for i in range(N)]
random.shuffle(indx)
df = pd.DataFrame([indx,x,y])
df = df.transpose()
df.columns = ['id','x','y']
```
- Now using the data frame, we find the product id which has x or y is higher than 0.5
- First, using regular for loop
```python
a_list = []
t0 = time.time()
for i in range(len(df)):
    if df.x.iat[i] > 0.5 or df.y.iat[i]> 0.5:
        a_list.append(df.id.iat[i])

print(len(a_list),  time.time()-t0)
```
    - This takes 2.29 sec in i3 Ubuntu desktop
- Now let's use Pythonic computing or vectorization
```
t0 = time.time(); bf = df.id[df.x.gt(0.5)|df.y.gt(0.5)] ; print(len(bf), time.time() - t0)
```
    - This one-liner takes 0.0049 sec
- Explain why there is more than 1000 times speed difference
    - Missing opportunities by unpredictable branches in cache memory
    - Overhead of append operation
    - Ref: https://stackoverflow.com/questions/16699247/what-is-a-cache-friendly-code
    
# R
- Preparation of testing data. Random data of product id and property x/y
```R
N <- 100000
x <- runif(N,0,1)
y <- runif(N,0,1)
idx <- sample(1:N)
df <- data.frame(idx,x,y)
```
- Now using the data frame, we find the product id which has x or y is higher than 0.5
- First, using regular for loop
```R
t0 <- Sys.time()
id_a <- c()
for (n in 1:dim(df)[1]) {
        if (df$x[n] > 0.5 | df$y[n] > 0.5) {
                id_a <- c(id_a, df$idx[n])
                }
}
cat(Sys.time() - t0)
```
    - This takes 8.8 sec in i3 Ubuntu desktop
- Now let's use vectorization
```R
t0 <- Sys.time(); id_b <- df$idx[df$x > 0.5 | df$y > 0.5]; cat(Sys.time() - t0)
```
    - This one-liner takes 0.0053 sec
- Explain why there is more than 1500 times speed difference


# MATLAB/Octave
- Initialization
```matlab
N = 100000;
idx = 1:N;
idx = idx(randperm(length(idx)));
x = rand(N,1);
y = rand(N,1);
```
- Regular loop
```matlab
tic
id_a = [];
for i=1:N
    if (x(i) > 0.5 || y(i) > 0.5)
        id_a = [id_a;idx(i)];
    end
end
toc
```
    - Takes 2.06 sec in i3 ubuntu desktop + Octave 4.0.0
- Vectorization
```matlab
tic
id_b = idx(x>0.5 | y> 0.5);
toc
```
    - Takes 0.004 sec in i3 Ubuntu desktop + Octave 4.0.0

# RUBY
```
N = 100000;
x = Array.new(N){ rand() }; nil
y = Array.new(N){ rand() }; nil
idx = [*1..N]; nil

start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
$i = 0
id_a = []
begin
  if x[$i] >0.5 or y[$i] > 0.5
    id_a.append($i)
  end
    $i += 1;
end until $i > N-1
finish = Process.clock_gettime(Process::CLOCK_MONOTONIC)
finish - start
```
- Took 0.012 sec. Ruby Array uses contiguous memor and avoids cache idling with loop
