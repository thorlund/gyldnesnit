d0 <- read.table("csv/yearcut0.csv", sep=",",header=TRUE)
d1 <- read.table("csv/yearcut1.csv", sep=",",header=TRUE)
d2 <- read.table("csv/yearcut2.csv", sep=",",header=TRUE)
d3 <- read.table("csv/yearcut3.csv", sep=",",header=TRUE)

png("billeder/yearcut0.png", height = 480, width = 800)
#barplot(d0$interessante.regioner,beside=TRUE,names=d0$ratios, angle = 45, cex.axis=1.0, cex.names = 1.4, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
 ## Increase bottom margin to make room for rotated labels
     #par(mar = c(7, 5, 5, 5) + 0.1)
     ## Create plot with no x axis and no x axis label
     barplot(d0$interessante.regioner,beside=TRUE, angle = 45, cex.axis=1.0, cex.names = 1.4, ylab = "Antal regioner"  , xaxt = "n",  xlab = "")
     ## Set up x axis with tick marks alone
     axis(1, labels = FALSE)
     ## Create some text labels
	 labels <- paste(names=d0$ratios, sep = " ")
#     labels <- paste("Label", 1:8, sep = " ")
     ## Plot x axis labels at default tick marks
     text(1:16, par("usr")[3]-1, srt = 45, adj = 1.1,
          labels = labels, xpd = TRUE)
     ## Plot x axis label at line 6 (of 7)
     mtext(1, text = "År", line = 6)
dev.off()
png("billeder/yearcut1.png", height = 480, width = 800)
barplot(d1$interessante.regioner,beside=TRUE,names=d1$ratios, cex.axis=1.0,  cex.names = 1.4, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/yearcut2.png", height = 480, width = 800)
barplot(d2$interessante.regioner,beside=TRUE,names=d2$ratios, cex.axis=1.0, cex.names = 1.4, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
png("billeder/yearcut3.png", height = 480, width = 800)
barplot(d3$interessante.regioner,beside=TRUE,names=d3$ratios, cex.axis=1.0,  cex.names = 1.4, xlab = "Snitratio i procent", ylab = "Antal regioner"  )
dev.off()
q()
