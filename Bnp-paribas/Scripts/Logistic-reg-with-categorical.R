
feature.names2 <- names(train)
twovars <- feature.names2[c(1,2)]
feature.namess2 <- feature.names2[-c(1,2)]
feature.namess2 <- feature.namess2[c(6,8,11,15,18,21,29,34,40,43,46,50,53,62,70,72,73,92,93,94,95,98,114,116,117,130,)]

feature.namess3 <- feature.names2[-c(1,2)]
feature.namess3 <- feature.namess3[c(3,22,24,30,31,38,47,52,62,66,71,72,74,75,79,91,6,8,11,15,18,21,29,34,40,43,46,50,53,62,70,72,73,92,93,94,95,98,114,116,117,130)]

feature.names1 <- feature.namess3
feature.names1 <- c(twovars,feature.names1)
trainlog <- train[,feature.names1]

feature.names1 <- feature.names1[-c(2)] # Removing target from feature names
testlog <- test[,feature.names1]

feature.names1 <- feature.names1[-c(1)] # Removing ID from feature names

h<-sample(nrow(trainlog),round(nrow(trainlog)*0.1))

trainlogt <- trainlog[-h,]
trainlogte <- trainlog[h,]

trainlogtID <- data.frame( ID= trainlogt$ID , trainlogt$target)
trainlogteID <- data.frame( ID= trainlogte$ID , trainlogte$target)

tra<-trainlog[,feature.names1]

logreg <- glm(trainlog$target[-h]~. , data = tra[-h,], family = binomial)

predval <- predict(logreg, tra[h,], type = "response")

trainlogteID <- data.frame(trainlogteID, predict = predval)

Lloss <- c()
for(i in 1:nrow(trainlogteID)){
  Lloss[i] <- logLoss(trainlogteID$trainlogte.target[i],trainlogteID$predict)
  Lloss <- append(Lloss,Lloss[i])
}

mean(Lloss)
