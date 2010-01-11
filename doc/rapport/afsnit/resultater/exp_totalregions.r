#!/usr/bin/env Rscript
#

d0 <- read.table("csv/exp_totalRegions.csv", sep=",", header=TRUE);
prod = d0$interessante.regioner*d0$antal;
prob = prod/sum(prod);
#print("Middelværdi");
#print(mean(d0$antal));
#print("Standardafvigelse");
#print(sd(d0$antal));
#print(sum(prod)/sum(d0$antal));

Regioner = c();
pos = 1;
start = 1;
for (i in d0$antal) {
    stop = start + i;
    s = seq(start, stop);
    for (j in s) {
        Regioner[j] = d0$interessante.regioner[pos];
    }
    pos = pos + 1;
    start = stop;
}
# Remove the last element
Regioner <- Regioner[1:length(Regioner) - 1];

print("Antal maleier");
print(sum(d0$antal));
print("Total regioner");
print(sum(prod));
print("Middelværdi");
print(mean(Regioner));
print("Standardafvigelse");
print(sd(Regioner));
#print(Regioner);
t.test(Regioner);

# Plot
png("billeder/exp_totalregions.png");
#plot(d0$interessante.regioner, d0$antal, "h", ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
barplot(d0$antal, beside=TRUE, names=d0$interessante.regioner, ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
#barplot(d0$antal,beside=TRUE, names=d0$interessante.regioner,cex.names=1)
dev.off();


# Plot
#png("billeder/exp_totalregions.png");
yval = seq(1,600);
#d0$antal[1] = 0;
#fval <- sum(d0$antal)*dnorm(yval, mean=mean(Regioner), sd=sd(Regioner));
#plot(d0$interessante.regioner, d0$antal, "h", ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
#points(yval, fval, type="l");
#dev.off();

#Regioner <- Regioner[299:length(Regioner)];
png("billeder/hist_exp_totalregions.png");
hist(Regioner, nclass=30, prob=TRUE);
#barplot(prob, beside=TRUE,cex.names=1)
#plot(d0$interessante.regioner, prob, "h", ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
#yval = seq(1,600);
#fval <- dexp(yval, rate = 1/(mean(Regioner)), log = FALSE)
fval <- dnorm(yval, mean=mean(Regioner), sd=sd(Regioner));
points(yval, fval, type="l");
dev.off();

#Regioner <- Regioner[2:length(Regioner)];
png("billeder/qq_exp_totalregions.png");
qqnorm(Regioner);
qqline(Regioner);
dev.off();
