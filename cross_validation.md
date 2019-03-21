## From datadojoscience training
- Test K(~10) tests using K-1 train buckets and 1 test buckets with K buckets of data
  - Different data yield different models (!!!) even in a SINGLE problem
- Highly different models (for test sets) mean there are high variance in data
  - Data cleaning or massage might be necessary
- Can evaluate which feature might be used/removed
  - Feature engineering
  - After all the features are determined, build the final model using all the K bucket
- In time series
  - Recent data is for test
  - Old data is for training
  - Shuffling recent data for training might not be good idea

# Sample R code
- Using caret package, cross validation is auotomated
```R
library(caret)
library(rpart.plot)

train <- read.csv("train.csv", stringsAsFactors=FALSE)
test <-read.csv("test.csv", stringsAsFactors = FALSE)

survived <- train$Survived
data.combined <- rbind(train[,-2], test)

data.combined$Pclass <- as.factor(data.combined$Pclass)
data.combined$Sex <- as.factor(data.combined$Sex)

train <- data.combined[1:891,]
train$Survived <- as.factor(survived)

test <- data.combined[892:1309,]

features <- c("Survived", "Sex", "Pclass","SibSp", "Parch" )
set.seed(12345)

##  use cross validation
caret.control <- trainControl(method="repeatedcv",
                              number = 10,
                              repeats=3)
rpart.cv <- train(Survived ~ ., 
                  data = train[, features],
                  method = "rpart",
                  trControl = caret.control,
                  tuneLength = 7)

rpart.cv
# 10*3*7 for cross validation. Final model is based on these 210 models.
# Therefore, it will make 211 models.

cat(paste("\n Cross validation standard deviation:", 
            sd(rpart.cv$resample$Accuracy), "\n", sep = " "))

rpart.best <- rpart.cv$finalModel

prp(rpart.best)
preds <- predict(rpart.cv, test, type = "raw")

submission <- data.frame(PassengerId = test$PassengerId, Survived=preds)

write.csv(submission, file="submission.csv", row.names=FALSE)
```
