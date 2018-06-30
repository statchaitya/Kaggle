feature.names2 <- names(train)
twovars <- feature.names2[c(1,2)]
feature.namess2 <- feature.names2[-c(1,2)]
feature.namess2 <- feature.namess2[c(6,8,11,15,18,21,29,34,40,43,46,50,53,62,70,72,73,92,93,94,95,98,114,116,117,130)]

feature.names1 <- feature.namess2

feature.names1 <- c(twovars,feature.names1)

trainlog <- train[,feature.names1]

feature.names1 <- feature.names1[-c(2)] # Removing target from feature names
testlog <- test[,feature.names1]

feature.names1 <- feature.names1[-c(1)] # Removing ID from feature names

logreg <- glm(trainlog$target~. , data = trainlog[,feature.names1], family = binomial)
pred <- predict(logreg, data = testlog[,feature.names1], type = "response")

submission <- data.frame(Id=test$ID, PredictedProb=pred)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Results/")
write.csv(submission,"Simple-xgb-2.csv",row.names=F)