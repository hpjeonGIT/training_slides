## Introduction to R
- Ref: https://en.wikipedia.org/wiki/R_(programming_language)
- Programming Language and software environment for statistical computing
	- Open-source (No license required!)
	- Programmable/script (like python)
		- Interpreted language
		- OOP
	- Plotting feature (like GNUplot)
	- Many libraries (like MATLAB)
		- Made by C/C++/Fortran
	- Available in Windows/Linux/OSX
	- HPC capability
		- Do parallel
		- Rmpi
		
## Using R
- R
  - For interactive operations
  - R CLI will appear
  - To exit, use: q()
- Rscript
  - For batch jobs or scripting
- rstudio
  - R studio GUI will pop-up

## Basics
- +, -, *, /, %% for algebra
- Assign using <-
-Create using =
- Logical F or T (or TRUE FALSE)
	- & or |
- Variable type using class(variable)
- Vector creation using c(1,2,3,4)
	- 2~4 component of a vector: some_vector[c(2:4)] 
		- some_vector[2:4] works too
		- some_vector[c(“tue”,”thurs”)] using names
- Assign names per vector component using names(variable) <- c(“mon”,”tue”,”wed”)
- Comparison using < or >
- Mean value using mean()

## Matrix
- Definition: matrix(1:8, byrow=TRUE, nrow=3)
- Assign row name: rownames(a_matrx) <- c(“row1”, “row2”)
- Assign column name: colnames(a_matrx) <- c(“col1”, “col2”)
	- Or matrix(c(), nrow=#,byrow=TRUE,dimnames=list(c_row, c_col))
- Sum of column data per row: rowSums()
- Sum of row data per column: colSums()
- Column bind: cbind()
- Row bind: rbind()
- Selection of matrix components
	- a_matrix[,1] = a_matrix[1:N,1] ## a_matrix[:,1] not work
	- a_matrix[,2] for second column data

## Factor
- Factorizes using factor(c(“pork”, “chicken”, “beef”))
	- Figures out the levels
- Enforces levels using 
	- factor(some_vector, order=TRUE, levels=c(“Low”, “Med”, “High”))
	- levels(some_vector) <- c(“Low”, “Med”, “High”)
		- Actual data can be shortened using “L”, “M”, “H” while the given levels have full names
- Summarize the vector status
	- General status: summary(some_vector)
	- Factored status: summary(factor(some_vector))
	- Factored vector can be compared using the order of the levels
		- factor_some_vector[3] > factor_some_vector[8]

## Dataframe
- head() or tail() for long data
- str() for the structure of the data
- Define Dataframe
	- n_vector<-c(1,2,3)
	- c_vector<-c(“a”,”b”,”c”)
	- l_vector<-c(F,F,T)
	- dframe <- data.frame(n_vector, c_vector, l_vector)
- dframe$l_vector
	- column name as the base vector name
- subset(dframe, subset=n_vector < 2.5)
	- Subsetting the dataset meeting the criterion
- order(dframe$n_vector, decreasing=TRUE)
	- Extract index in the order of the condition

## List/Dataframe
- a_list <- list(a_vector, a_matrx, a_dframe)
- names(a_list) <- c(“alpha”, “beta”, “gamma”)
- df <- data.frame(dataset$c1, dataset$c2, …)
- colnames(df) <- c(“time”, “sales”, “weather”, …)
- cleaned_data <- df[complete.cases(df),]
	- Remove NA terms
- Random sampling of data sets
	- intrain <- createDataPartition(y=cleaned_data$time, p=0.5, list=FALSE)
	- training <- cleaned_data[intrain,]
	- testing <- cleaned_data[-intrain,]

## Sample prediction steps
```R
> data(iris)
> ls()
[1] "iris"
> library(caret)
> intrain <-createDataPartition(y=iris$Species,p=0.5, list=FALSE)
> training <- iris[intrain,]
> testing <- iris[-intrain,]


> str(iris)
'data.frame':   150 obs. of  5 variables:
 $ Sepal.Length: num  5.1 4.9 4.7 4.6 5 5.4 4.6 5 4.4 4.9 ...
 $ Sepal.Width : num  3.5 3 3.2 3.1 3.6 3.9 3.4 3.4 2.9 3.1 ...
 $ Petal.Length: num  1.4 1.4 1.3 1.5 1.4 1.7 1.4 1.5 1.4 1.5 ...
 $ Petal.Width : num  0.2 0.2 0.2 0.2 0.2 0.4 0.3 0.2 0.2 0.1 ...
 $ Species     : Factor w/ 3 levels "setosa","versicolor",..: 1 1 1 1 1 1 1 1 1 1 ...
> str(training)
'data.frame':   75 obs. of  5 variables:
 $ Sepal.Length: num  4.7 4.6 5 5.4 4.4 4.8 4.3 5.7 5.4 5.1 ...
 $ Sepal.Width : num  3.2 3.1 3.6 3.9 2.9 3 3 4.4 3.9 3.5 ...
 $ Petal.Length: num  1.3 1.5 1.4 1.7 1.4 1.4 1.1 1.5 1.3 1.4 ...
 $ Petal.Width : num  0.2 0.2 0.2 0.4 0.2 0.1 0.1 0.4 0.4 0.3 ...
 $ Species     : Factor w/ 3 levels "setosa","versicolor",..: 1 1 1 1 1 1 1 1 1 1 ...
> str(testing)
'data.frame':   75 obs. of  5 variables:
 $ Sepal.Length: num  5.1 4.9 4.6 5 4.9 5.4 4.8 5.8 5.7 5.1 ...
 $ Sepal.Width : num  3.5 3 3.4 3.4 3.1 3.7 3.4 4 3.8 3.8 ...
 $ Petal.Length: num  1.4 1.4 1.4 1.5 1.5 1.5 1.6 1.2 1.7 1.5 ...
 $ Petal.Width : num  0.2 0.2 0.3 0.2 0.1 0.2 0.2 0.2 0.3 0.3 ...
 $ Species     : Factor w/ 3 levels "setosa","versicolor",..: 1 1 1 1 1 1 1 1 1 1 ...
 > knn_model <- train(Species~., method="knn",data=training)
> knn_pred <- predict(knn_model,testing)

> table(knn_pred,testing$Species)

knn_pred     setosa versicolor virginica
  setosa         25          0         0
  versicolor      0         22         2
  virginica       0          3        23

> rf_model <- train(Species~., method="rf", data=training)
> rf_pred <- predict(rf_model, testing)
> table(rf_pred, testing$Species)

rf_pred      setosa versicolor virginica
  setosa         25          0         0
  versicolor      0         21         2
  virginica       0          4        23


> library(e1071)
> svm_model <- svm(Species ~., data=training)
> svm_pred <- predict(svm_model, testing)
> table(svm_pred, testing$Species)

svm_pred     setosa versicolor virginica
  setosa         25          0         0
  versicolor      0         23         2
  virginica       0          2        23

```

## HPC of R
- DO parallel
	- doSNOW, doMC ... using SMP architecture
	- Within a single node
```R
library(doMC)
num_cpus = 10
registerDoMC(num_cpus)
tmp <- foreach(i = 1:Nloop,.packages=c("e1071","FSelector","kknn")) %dopar%
{
subset = rep(0, len)
subset[child_comb[, i]] = 1
result = eval.fun(attributes[as.logical(subset)])
                        result
}
```
- Rmpi
	- MPI wrapper for R
	- Most of MPI functions are available
	- Only batch
```R
library(Rmpi)
myid <- mpi.comm.rank(comm=0)
ncpu <- mpi.comm.size(comm=0)
i_init = as.integer(as.numeric(myid)*Nloop/ncpu + 1)  
i_fin  = as.integer(as.numeric(myid+1)*Nloop/ncpu)    
N_seg  = i_fin - i_init + 1                           
for(i in i_init:i_fin) 
{
…
}
tmp  <- mpi.allreduce(best$result, type=2, op="maxloc", comm=0)
mpi.barrier(comm=0)
mpi.quit()
```
## Using R in jupyter-notebook
-Add R into jupyter notebook
	- install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'), dependencies=TRUE, lib="/usr/nic/R/3.5.1/lib64/R/library")
	- devtools::install_github('IRkernel/IRkernel')
	- IRkernel::installspec()
	- This will make ir folder in /home/user/.local/share/jupyter/kernels. Then copy the ir folder into /share/python/3.6.6/share/jupyter/kernels/
- Using KerasR
	- install.packages('reticulate')
	- library(reticulate)
	- use_python("/share/python/3.6.6/bin/python3")
	- install.packages('kerasR')
- May provide  .Renviron at $HOME
	- RETICULATE_PYTHON=/share/python/3.6.6/bin/python3
