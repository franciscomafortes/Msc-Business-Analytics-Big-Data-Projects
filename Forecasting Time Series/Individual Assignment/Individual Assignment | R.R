############################# Individual Assignment: Forecasting Time Series ####################################

library(fBasics)
library(forecast) 

# Set the folder (path) that contains this R file as the working directory
dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)

# *** MULTIPLICATIVE SARIMA MODELS ***
  
data<-read.csv("/Users/kuka/Desktop/Datos\ CO2.csv")
y<-data[,4] 

ts.plot(y)

nlags=120     # play with this parameter..

par(mfrow=c(3,1)) # plot the series, its acf and pacf together
ts.plot(y)   
acf(y)
pacf(y)

mean(y) # compute basic statistics
sd(y)
skewness(y)
kurtosis(y,method=c("moment"))  


s=12      # seasonal parameter 

nsdiffs(y,m=s,test=c("ocsb"))  # seasonal differences? big D
ndiffs(y, alpha=0.05, test=c("adf")) # regular differences? small d

#Shapiro test
shapiro.test(y)

#Box-Test
Box.test (y, lag = 20, type="Ljung")

#Checking for normality graphically
hist(y,prob=T,ylim=c(0,0.6),xlim=c(mean(y)-3*sd(y),mean(y)+3*sd(y)),col="red")
lines(density(y),lwd=2)
mu<-mean(y)
sigma<-sd(y)
x<-seq(mu-3*sigma,mu+3*sigma,length=100)
yy<-dnorm(x,mu,sigma)
lines(x,yy,lwd=2,col="blue")

#Differences of regular
z<-diff(y)

par(mfrow=c(3,1))
ts.plot(z) 
acf(z)  
pacf(z) ##ACF slow decay to 0 PACF at 8


#LOG

par(mfrow=c(3,1))
ts.plot(log(y))
acf(log(y),nlags)
pacf(log(y),nlags)  

nsdiffs(log(y),m=s,test=c("ocsb"))  # seasonal differences? big D
ndiffs(log(y), alpha=0.05, test=c("adf")) # regular differences? small d

yy<- log(y)

fity<-arima(yy[1:83],order=c(1,1,0),seasonal=list(order=c(0,1,1),period=s))
fityy<-arima(yy,order=c(1,1,0),seasonal=list(order=c(0,1,1),period=s))


par(mfrow=c(3,1))
ts.plot(fityy$residuals)
acf(fityy$residuals,nlags)
pacf(fityy$residuals,nlags)    
``
ndiffs(fityy$residuals, alpha=0.05, test=c("adf")) # regular differences?
nsdiffs(fityy$residuals, m=s,test=c("ocsb")) # seasonal differences?


Box.test(fityy$residuals,lag=30)


shapiro.test(fityy$residuals)  

# estimate the SAR and analyze the estimated parameters. Compare with the Seasonal Difference
fit<-arima(y,order=c(8,1,0),seasonal=list(order=c(0,0,1),period=s)) 
goodfit<-arima(y[1:83],order=c(0,1,0),seasonal=list(order=c(1,1,0),period=s)) 
badfit<-arima(y[1:83],order=c(0,0,3),seasonal=list(order=c(0,1,0),period=s)) 
fit

par(mfrow=c(3,1))
ts.plot(fit$residuals)
acf(fit$residuals,nlags)
pacf(fit$residuals,nlags)    
``
ndiffs(fit$residuals, alpha=0.05, test=c("adf")) # regular differences?
nsdiffs(fit$residuals, m=s,test=c("ocsb")) # seasonal differences?


Box.test(fit$residuals,lag=30)

   
shapiro.test(fit$residuals)  

# 0.01 for the first series
# 1 for the second series

hist(fit$residuals,prob=T,xlim=c(mean(fit$residuals)-3*sd(fit$residuals),mean(fit$residuals)+3*sd(fit$residuals)),col="red")
lines(density(fit$residuals),lwd=2)
mu<-mean(fit$residuals)
sigma<-sd(fit$residuals)
x<-seq(mu-3*sigma,mu+3*sigma,length=100)
yy<-dnorm(x,mu,sigma)
lines(x,yy,lwd=2,col="blue")

y.pred<-predict(fit,n.ahead=12)
y.pred$pred   # point predictions
y.pred$se    # standard errors

ts.plot(y.pred$pred)  # see how the model captures the seasonality

# point predictions and standard errors

y.pred<-predict(fit,n.ahead=24)
y.pred$pred   # point predictions
y.pred$se    # standard errors


# plotting real data with point predictions

new <- c(y[1:83],y.pred$pred) # real data + predicted values

plot.ts(new,main="Predictions",ylim=c(min(y),max(y)),
        ylab="Q Earn Per Share",col=3,lwd=2) # time series plot
lines(y,col=4,lwd=2) # for the second series
legend("topleft",legend=c("Predictions","Historical"),col=c(3,4),
       bty="n",lwd=2)


par(mfrow=c(1,1))
# point predictions and standard errors

g.pred<-predict(goodfit,n.ahead=24)
g.pred$pred   # point predictions
g.pred$se    # standard errors
b.pred<-predict(badfit,n.ahead=24)
b.pred$pred   # point predictions
b.pred$se    # standard errors
l.pred<-predict(fity,n.ahead=24)
l.pred
l.pred$pred   # point predictions
l.pred$se    # standard errors

summary(goodfit)
summary(badfit)
summary(fity)

mae<-function(pred,test){
  err<-0
  for(i in 1:length(pred)){
    err=err+abs(pred[i]-test[i])
  }
  return(err/length(test))
}
mae(g.pred$pred,y[84:107])
mae(b.pred$pred,y[84:107])
mae(exp(l.pred$pred),y[84:107])

# plotting real data with point predictions

bew <- c(y[1:83],b.pred$pred) # real data + predicted values
gew <- c(y[1:83],g.pred$pred) # real data + predicted values
lew <- c(y[1:83],exp(l.pred$pred)) # real data + predicted values

plot.ts(bew,main="Predictions",ylim=c(min(y),max(y)),
        ylab="Q Earn Per Share",col=2,lwd=2) # time series plot
lines(gew,col=3,lwd=2) # for the second series
lines(lew,col=5,lwd=2)
lines(y,col=4,lwd=2) # for the second series

legend("topleft",legend=c("Real","(0,1,0)x(1,1,0)4","(0,0,3)x(0,1,0)4","log((1,1,0)x(0,1,1)4)"),col=c(4,3,2,5),
       bty="n",lwd=2)


#ERROR
n<-length(y)


n.estimation<-120 # 
n.forecasting<-n-n.estimation # 198 observations
horizontes<-12 # number of periods ahead

predicc<-matrix(0,nrow=n.forecasting,ncol=horizontes)
real<-matrix(0,nrow=n.forecasting,ncol=1)
real<-y[(n.estimation+1):length(y)] 
MSFE<-matrix(0,nrow=horizontes,ncol=1)
MAPE<-matrix(0,nrow=horizontes,ncol=1)

for (Periods_ahead in 1:horizontes) {
  for (i in 1:n.forecasting) {
    aux.y<-y[1:(n.estimation-Periods_ahead+i)];
    fit<-arima(y,order=c(8,1,0),seasonal=list(order=c(0,0,1),period=s));
    y.pred<-predict(fit,n.ahead=Periods_ahead);
    predicc[i,Periods_ahead]<- y.pred$pred[Periods_ahead];
  }
  error<-real-predicc[,Periods_ahead];
  MSFE[Periods_ahead]<-mean(error^2);
  MAPE[Periods_ahead]<-mean(abs(error/real)) *100;
}
MSFE;
MAPE;








