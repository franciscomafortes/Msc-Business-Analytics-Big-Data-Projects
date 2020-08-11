############################ MBD 2019 OCT S1_Group E Assignment ##################################
############################### December 9th,2019 ##################################

############################### [PART 1] EDA ##################################

folder_path<-"/Users/MenaL/Desktop/GROUP P/R_project"
solar<-readRDS("/Users/MenaL/Desktop/GROUP P/R_project/solar_dataset.RData")
add<-readRDS("/Users/MenaL/Desktop/GROUP P/R_project/additional_variables.RData")
geo<- read.table(file.path(folder_path, "station_info.csv"), sep = ",", header = TRUE)
geo

str(solar)
dim(solar)
str(add)
dim(add)

solar[,1:100]
as.data.frame(sapply(add[,2:101], summary)); 

##Separate Train, Validation, Test & Predict datasets
train_station<-solar[1:5113,1:99]
val_pca<-solar[,100:ncol(solar)]
val_pca_2<-solar[5114:nrow(solar),100:ncol(solar)]
## These three datasets do not have "NA"s.

test<-solar[5114:nrow(solar),1:99]
## Predict set has all the "NA"s.

############################### [1.1] Basic DATA CLEANING ###################
############################### [1.1.1] Check Constant variables ###################
train_station
n_unique_values_f <- function(x){
  return(length(unique(x)));
}

sapply(train_station, n_unique_values_f);
sapply(val_pca, n_unique_values_f);
sapply(test, n_unique_values_f);
## The Train_station sample does not have constant variables, and further, pca sets of data have non repetitive values.

#check for additional_variables table
sapply(add,n_unique_values_f)
#no constant variables from addtional_variables table

############################### [1.1.2] Check NAs  ###################
count_nas <- function(x){
  ret <- sum(is.na(x));
  return(ret);
}

sapply(train_station, count_nas)
sapply(val_pca, count_nas)
sapply(test, count_nas)
## These three datasets do not have "NA"s.
sapply(add, count_nas)
nrow(add)

na_p<-as.data.table(sapply(add, function(x){100*sum(is.na(x))/length(x)}))

na_perc<-sort(na_p$V1,decreasing=T)

#Since most of the addtional variables measures "importance" of other variables, fill missing values with mode is chosen.
my_mode <- function(x) {
  ret <- as.numeric(names(sort(table(x), decreasing = TRUE))[1])
  return(ret);
}

fill_missing_values <- function(x){
    x[is.na(x)] <- my_mode(x)
  return(x);
}

add2<-data.frame(sapply(add, fill_missing_values),stringsAsFactors = F)
add3<-as.data.frame(lapply(add2, type.convert, as.is = TRUE)) ##casting add2 back to numeric class.

##add3 is the cleaned table without NAs

############################### [1.1.3] Reduce PCAs--Bin 357 PCs (weather variables) ###################
val_pca<-solar[1:5113,100:ncol(solar)]

sapply(val_pca, function(x){length(unique(x))})
dim(pca_stats_2)
pca_stats<-as.data.frame(sapply(val_pca, summary)); 

library(OneR)
bin_pca_1<-bin(pca_stats_2, nbins = 53, labels = NULL, method = c("length", "content",
                                               "clusters"), na.omit = TRUE)

bin_pca_2<-bin(pca_stats_2, nbins = 54, labels = NULL, method = c("length", "content",
                                                                "clusters"), na.omit = TRUE)


frequencies_1 <- table(bin_pca_1$`Median`);
frequencies_2 <- table(bin_pca_2$`Median`);

levels(bin_pca_1$`Median`)
levels(bin_pca_2$`Median`)

a<-sum(bin_pca_1$`Median`==levels(bin_pca_1$`Median`)[16])
b<-sum(bin_pca_1$`Median`==levels(bin_pca_1$`Median`)[17])
colnumber<-ncol(val_pca)-a-b
colnumber


barplot(frequencies_1, col = "blue",font = 1, las = 2,cex.axis=1);

barplot(frequencies_2, col = "blue",font = 1, las=2, cex.axis=1);

boxplot(pca_stats, col = "blue");

################################## [1.2]  Compute Correlation #############################

############# [1.2.1] Correlation between Solar Energy & Elevations of the station ##################
station_mean<-descr_stats[4,]
str(station_mean)
s_m<-t(station_mean)
elev<-geo$elev
energy_elev<- cbind(s_m,data.frame(elev) );
cor(energy_elev,x="Mean",y="elev", method = "pearson")

library("ggpubr")
ggscatter(energy_elev, x = "Mean", y = "elev", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Solar Energy in (J m-2)", ylab = "Eelevation of Each Station (Meters)")

correlation1<-cor.test(energy_elev$Mean, energy_elev$elev, 
                       method = "pearson")
correlation1$p.value
correlation1$conf.int

######The p-value of the test is 2.47607910^{-28}, 
######which is less than the significance level alpha = 0.05. 
######The conclusion can be made that solar energy and the elevation of the station
######are significantly correlated with a correlation coefficient of 0.85 and p-value of 2.47607910^{-28}.


############# [1.2.2] Correlation between higher latitude and smaller output? ##################

##using mean ##really bad result
s_m<-t(station_mean)
lat<-geo$nlat
energy_lat<- cbind(s_m,data.frame(lat) );
energy_lat
str(energy_lat)

library("ggpubr")
ggscatter(energy_lat, x = "Mean", y = "lat", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Solar Energy in (J m-2)", ylab = "Latitude of Each Station (degree)")

correlation2<-cor.test(energy_lat$Mean, energy_lat$lat, 
                       method = "pearson")

##using sum ##still bad result
sum<-as.data.frame(sapply(dt, sum))
names(sum)<-"sum"
sum
lat<-geo$nlat
energy_lat_s<- cbind(sum,data.frame(lat) );
energy_lat_s


library("ggpubr")
ggscatter(energy_lat_s, x = "sum", y = "lat", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Total Solar Energy in (J m-2)", ylab = "Latitude of Each Station (degree)")

correlation3<-cor.test(energy_lat_s$sum, energy_lat_s$lat, 
                       method = "pearson")

ggpairs(energy_lat_s)   


##################################[1.2.3] Try with MULTICOLLINEARITY#########################
library(ggplot2)
install.packages("GGally")
library(GGally)
install.packages("faraway");
minisolar <- solar[,100:length(solar)];
pairs(minisolar[,1:3], col="dodgerblue",gap = 1/2);
correlations <- round(cor(minisolar), 4);

ggpairs(minisolar[,1:3])   



############################### [1.3] Basic Descriptive Statistics and Outliers of Solar Energy Production dataset ###################
############## [1.3.1] Descriptive Statistics of each weather station's solar energy production from 1994-01-01 to 2007-12-31 ############
dt<-train_station[,1:98]


ggplot(best_solar_production, aes(x = Date, y = IDAB))+theme_bw() +
  geom_point()

ggplot(best_solar_production, aes(x = Date, y = ALTU))+theme_bw() +
  geom_point()
ggplot(best_solar_production, aes(x = Date, y = BESS))+theme_bw() +
  geom_point()

best_solar_production<-solar[1:5113,1:99]

###Other plots
ggplot(as.data.frame(dt), aes(x=ACME)) + geom_density()
ggplot(dt, aes(x=ACME)) + geom_histogram(binwidth=300000)

############## [1.3.2] Outliers ###########
###### outlier 1
install.packages("~/Downloads/outliers_0.13-3.tar")
library(outliers)
outlier1<-outlier(dt, opposite = T, logical =F)
outlier1
outlier2<-outlier(dt, opposite = F, logical =F)



#### Maximum of the max
descr_stats<-as.data.frame(sapply(dt, summary)); 
descr_stats[which.max(descr_stats["Max.",])]

max<-as.data.frame(t(descr_stats["Max.",]))
class(max)
summary(max)
stations<-rownames(max)
max<-cbind(max,as.data.frame(stations))
ggplot(as.data.frame(max),aes(y=Max.,x=stations))+geom_point()

#######Outlier treatment
IDAB_max<-sort(dt[,IDAB],decreasing = T)
lmax<-IDAB_max[3]

class(lmax)

dt[dt[,IDAB]==outlier2["IDAB"],IDAB]<-lmax

dt[dt[,IDAB]==IDAB_max[2],IDAB]<-lmax


############## [1.3.3] GIS Visualization ###########

############# Basic interactive map #################
### uploaded on: http://rpubs.com/n_men/map 
install.packages("leaflet")
install.packages("geojsonio")
install.packages("rgdal")
library(rgdal)
library(leaflet)


leaflet() %>% addTiles() %>% addMarkers(
  lng=geo$elon, 
  lat=geo$nlat,
  clusterOptions = markerClusterOptions(freezeAtZoom = 6),
  label = geo$stid
)

#%>%
#  addPolygons(
#   fillColor = ~pal(gis1$avg),
#  weight = 2,
# opacity = 1,
#color = "white",
#dashArray = "3",
#fillOpacity = 0.7)

############# Mapping of size of production/"density" of the solar farms #################
average_sun<-function(x){
  res<-sum(x)
  return(res)
}

avg_sun<-as.data.frame(sapply(dt, average_sun)); 
colnames(avg_sun)<-"avg"
gis1<- cbind(avg_sun,data.frame(lng=geo$elon,lat=geo$nlat))

leaflet(gis1) %>% addTiles() %>%
  addCircles(lng =~lng, lat = ~lat, weight = 0.5,
             radius = ~sqrt(avg)*0.12
  )


############################### [1.4] Basic Descriptive Statistics of Additional Variable dataset ###################
descr_stats_add<-as.data.frame(sapply(add2, summary)); 

ggplot(add2, aes(x = Date, y = V6409))+theme_bw() +geom_point(color = "#00AFBB")+labs(subtitle="Additional Variable V6409",y="V6409", x="Dates")

ggplot(add2, aes(x=V6409)) + geom_histogram(binwidth=4,fill ="#C3D7A4")+labs(subtitle="Histogram of V6409",y="Counts", x="Dates")
