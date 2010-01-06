#!/usr/bin/env Rscript
#

d0 <- read.table("csv/totalRegions.csv", sep=",", header=TRUE);
prod = d0$interessante.regioner*d0$antal;
#barplot(d0$antal,beside=TRUE, names=d0$interessante.regioner,cex.names=1)
#print("Middelværdi");
#print(mean(d0$antal));
#print("Standardafvigelse");
#print(sd(d0$antal));
print(sum(prod)/sum(d0$antal));

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
Regioner <- Regioner[1:length(Regioner) - 1];
print(Regioner);
print(length(Regioner));
print(sum(d0$antal));
print("Middelværdi");
print(mean(Regioner));
print("Standardafvigelse");
print(sd(Regioner));

# Plot
png("billeder/totalregions.png");
d0$antal[1] = 0;
plot(d0$interessante.regioner, d0$antal, "h", ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
dev.off();

png("billeder/hist_totalregions.png");
hist(Regioner, nclass=15, prob=TRUE);
#yval = seq(1,600);
#fval <- dnorm(yval, mean=mean(obs), sd=sd(obs));
#points(yval, fval, type="l");
dev.off();
