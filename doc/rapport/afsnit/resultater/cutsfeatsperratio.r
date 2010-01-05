d0 <- read.table("csv/cut0featsperratio.csv", sep=",", header=TRUE)
d1 <- read.table("csv/cut1featsperratio.csv", sep=",", header=TRUE)
d2 <- read.table("csv/cut2featsperratio.csv", sep=",", header=TRUE)
d3 <- read.table("csv/cut3featsperratio.csv", sep=",", header=TRUE)
d4 <- read.table("csv/cut0cut1eatsperratio.csv", sep=",",header=TRUE)
d5 <- read.table("csv/cut2cut3eatsperratio.csv", sep=",",header=TRUE)

png("billeder/cut0featsperratio.png")
barplot(d0$interessante.regioner,beside=TRUE, names=d0$ratios, cex.axis=1.0, cex.names = 1, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/cut1featsperratio.png")
barplot(d1$interessante.regioner,beside=TRUE, names=d1$ratios, cex.axis=1.0, cex.names = 1, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/cut2featsperratio.png")
barplot(d2$interessante.regioner,beside=TRUE, names=d2$ratios, cex.axis=1.0, cex.names = 1, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/cut3featsperratio.png")
barplot(d3$interessante.regioner,beside=TRUE, names=d3$ratios, cex.axis=1.0, cex.names = 1, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/cut0cut1eatsperratio.png")
barplot(d4$interessante.regioner,bedside=TRUE,names=d4$ratios, cex.axis=1.0, cex.names = 0.7, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/cut2cut3eatsperratio.png")
barplot(d5$interessante.regioner,beside=TRUE,names=d5$ratios, cex.axis=1.0,  cex.names = 0.7, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
q()
