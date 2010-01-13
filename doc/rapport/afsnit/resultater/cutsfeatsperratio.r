d2 <- read.table("csv/G_vs_totradjedele.csv", sep=",",header=TRUE)
d1 <- read.table("csv/G_vs_totradjedeleU.csv", sep=",",header=TRUE)


png("billeder/G_vs_to_tredjedeleU.png", height = 480, width = 480)
barplot(d1$interessante.regioner,beside=TRUE,names=d1$ratios, cex.axis=1.0,  cex.names = 1.4, xlab = "Gyldne snit og to tredjedele", ylab = "Antal regioner"  )
dev.off()
png("billeder/G_vs_to_tredjedele.png", height = 480, width = 480)
barplot(d2$interessante.regioner,beside=TRUE,names=d2$ratios, cex.axis=1.0,  cex.names = 1.4, xlab = "Gyldne snit og to tredjedele", ylab = "Antal regioner"  )
dev.off()
q()
