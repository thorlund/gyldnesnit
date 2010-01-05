#!/usr/bin/env Rscript
#

d0 <- read.table("csv/totalRegions.csv", sep=",", header=TRUE);
png("billeder/totalregions.png");
#barplot(d0$antal,beside=TRUE, names=d0$interessante.regioner,cex.names=1)
plot(d0$interessante.regioner, d0$antal, "h", ylab="Antal malerier", xlab="Antal fundne insteressante regioner");
dev.off();
