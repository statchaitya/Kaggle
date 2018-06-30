# A script for trying out models on different subsets of features and saving the CV results.
# FEATURE SELECTION
rm(list = ls())
set.seed(666)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/Original/")
require(xgboost)

# Import and arrange the required data

train <- read.csv('train01-NA-imputed.csv',header=T)
test <- read.csv('test01-NA-imputed.csv',header=T)

trfeat <- read.csv('some-interactions-tr-02.csv',header=T)
tefeat <- read.csv('some-interactions-te-02.csv',header=T)

#Each and every variable name has to be the same, if not, some adjustments need to be
# mad
names(trfeat)[c(13,14)] = c("v10xlog1pv50","v50xlog1pv50")
names(tefeat)[c(13,14)] = c("v10xlog1pv50","v50xlog1pv50")

#train_l <- list()
#test_l <- list()
clfcv1 <- list()
#l <- list()
#t <- list()

comb2 <-(combn(14,2,simplify = TRUE))

comb2df<-as.data.frame(comb2)

v1<-comb2df[1,]
v2<-comb2df[2,]

v1<-c(v1)
v2<-c(v2)

v1 <- as.numeric(v1)
v2 <- as.numeric(v2)

param <- list(  objective           = "reg:logistic", 
                booster = "gbtree",
                "eval_metric" = "logloss",
                eta                 = 0.02, # 0.06, #0.01,
                max_depth           = 11, #changed from default of 8
                subsample           = 0.96, # 0.7
                colsample_bytree    = 0.45, # 0.7
                min_child_weight = 1,
                num_parallel_tree   = 1
                # alpha = 0.0001, 
                # lambda = 1
)

models <- function(x){
  train1 <- cbind(train,trfeat[,x[1]],trfeat[,x[2]])
  test1 <- cbind(test,tefeat[,x[1]],tefeat[,x[2]])
  
  names(train1)[107] = names(trfeat)[x[1]]
  names(train1)[108] = names(trfeat)[x[2]]
  
  names(test1)[106] = names(tefeat)[x[1]]
  names(test1)[107] = names(tefeat)[x[2]]
  
  feature.names <- names(train1)[-c(1,2)]
  
  tra<-train1[,feature.names]
  
  dtrain<-xgb.DMatrix(data=data.matrix(tra),label=train1$target)
  
  clfcv <- xgb.cv(params = param,
                  data = dtrain,
                  nrounds = 100,
                  nfold = 5,
                  prediction = FALSE,
                  print.every.n = 20,
                  early.stop.round = 50)
  
  clfcv <- data.frame(clfcv)
  bestrow = which(clfcv[,3]== min(clfcv[,3]))
  
  dftemp <- clfcv[bestrow,]
  assign(paste(names(train1)[107],names(train1)[108], sep = "_"), dftemp)
  
  setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Valresults/")
  write.csv(dftemp,paste(paste(names(train1)[107],names(train1)[108], sep = "_"),'.csv',sep=""), row.names = F)
  
  rm(train1,test1,feature.names,dtrain,dftemp,bestrow)
  
}

combn(14,2,models)
