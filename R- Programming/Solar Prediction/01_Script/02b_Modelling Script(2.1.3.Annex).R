folder_path<-"/Users/MenaL/Desktop/GROUP P/R_project"
solar<-readRDS("/Users/MenaL/Desktop/GROUP P/R_project/solar_dataset.RData")
add<-readRDS("/Users/MenaL/Desktop/GROUP P/R_project/additional_variables.RData")
geo<- read.table(file.path(folder_path, "station_info.csv"), sep = ",", header = TRUE)
library(data.table)

write.csv(solar, "/Users/MenaL/Desktop/GROUP P/R_project/solar_dataset.csv",
          quote = F, row.names = F)

################################## BUILD elevation non-constant  DATATABLE #######################################
solar[solar$IDAB==39442800,]$IDAB<-30795000
solar[solar$IDAB==32855400,]$IDAB<-30795000
station<-as.data.frame(solar[1:5113,1:99],stringsAsFactors = F)

station_t_s<-as.data.frame(t(station),stringsAsFactors = F)

##change back to numeric after t()
station_t<-as.data.frame(lapply(station_t_s, type.convert, as.is = TRUE))

pca<-as.data.frame(solar[1:5113,100:117],stringasFactors=F)


prepare<-station_t[2:99,]

new_all<-data.frame()


for (i in 1:5113) {
  new_df<-data.frame()
  new_df<-as.data.frame(prepare[,i],stringsAsFactors = FALSE)
  new_df<-cbind(new_df,as.data.frame(pca[i,1:18]),as.data.frame(geo$elev))
  new_all<-rbind(new_all,new_df)
}


names(new_df)[1]<-"solar_p"
names(new_df)[20]<-"elev"

################################## BUILD MODEL ######################################
set.seed(100); 
train_index_1<- sample(1:nrow(new_df), 0.7*nrow(new_df)); 
train_1<- new_df[train_index_1,]
test<-new_df[-train_index_1,]

production<-lm(solar_p~ PC1+PC2+PC3+PC4+PC5+PC6+PC7+PC8+PC9+PC10+PC11+PC12+PC13+PC14
           +PC15+PC16+PC17+PC18+elev, data=train_1)

predictions_test <- predict(production, newdata = test)
predictions_train<-predict(production, newdata = train_1)

errors_test <- predictions_test - test$solar_p
errors_train<-predictions_train-train_1$solar_p

mae_test<- round(mean(abs(errors_test)), 2);
mae_train<- round(mean(abs(errors_train)), 2);

mse_test<- round(mean(errors_test^2), 2);
mse_train<- round(mean(errors_train^2), 2);


