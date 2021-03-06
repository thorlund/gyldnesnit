d0 <- read.table("csv/nation.csv", sep=",",header=TRUE)
d1 <- read.table("csv/nationcutU.csv", sep=",",header=TRUE)

png("billeder/nation.png", height = 480, width = 800)
par(las=3, lheight =6, mai=c(2,1,1,1))
barplot(d0$interessante.regioner,beside=TRUE,names=d0$ratios,  cex.axis=1.0, cex.names = 1.4, ylab = "Antal Billeder" )
par(las=1)
mtext(1, text = "Skole", line = 8)
dev.off()

png("billeder/nationcutU.png", height = 480, width = 800)
par(las=3, lheight =6, mai=c(2,1,1,1))
barplot(d1$interessante.regioner,beside=TRUE,names=d1$ratios, cex.axis=1.0,  cex.names = 1.4, ylab = "Gennemsnitlig antal regioner"  )
par(las=1)
mtext(1, text = "Skole", line = 8)
dev.off()
q()
