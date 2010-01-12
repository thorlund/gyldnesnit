d0 <- read.table("csv/nationNrImage.csv", sep=",",header=TRUE)
d1 <- read.table("csv/yearNrImage.csv", sep=",",header=TRUE)

png("billeder/nationNrImage.png", height = 480, width = 800)
par(las=3, lheight =6, mai=c(2,1,1,1))
barplot(d0$interessante.regioner,beside=TRUE,names=d0$ratios,  cex.axis=1.0, cex.names = 1.4, ylab = "Antal malerier" )
par(las=1)
mtext(1, text = "Nationalitet", line = 8)
dev.off()

png("billeder/yearNrImage.png", height = 480, width = 800)
par(las=3, lheight =6, mai=c(2,1,1,1))
barplot(d1$interessante.regioner,beside=TRUE,names=d1$ratios, cex.axis=1.0,  cex.names = 1.4, ylab = "Antal malerier"  )
par(las=1)
mtext(1, text = "År", line = 8)
dev.off()
q()
