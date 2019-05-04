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
