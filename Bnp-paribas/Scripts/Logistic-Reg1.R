

f <- c()
for (i in 1:ncol(train)){
  if (is.numeric(train[, i])) f <- c(f,i)
}
feature.names1 <- names(train)[f]
trainlog <- train[,feature.names1]

feature.names1 <- feature.names1[-c(2)] # Removing target from feature names
testlog <- test[,feature.names1]

feature.names1 <- feature.names1[-c(1)] # Removing ID from feature names

logreg <- glm(trainlog$target~. , data = trainlog[,feature.names1], family = binomial)
pred <- predict(logreg, data = testlog[,feature.names1], type = "response")


