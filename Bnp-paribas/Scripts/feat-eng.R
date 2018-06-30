setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Feateng/")

predtrain <- predict(logreg, trainlog[, feature.names1], type = "response")
feateng1train <- data.frame(ID = trainlog$ID,  feature1 = predtrain)
write.csv(feateng1train, "feateng1-train.csv", row.names = F)

rm(predtrain)

predtrain1 <- predict(logreg,testlog[, feature.names1], type = "response")
feateng1test <- data.frame( ID = testlog$ID, feature1 = predtrain1)
write.csv(feateng1test, "feateng1-test.csv", row.names = F)
