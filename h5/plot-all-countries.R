data = read.csv("firearms.csv", header=T, sep=",")
OECDrows = data[,"OECD"]=="Y"

# uncomment this line to display only OECD countries
#data = data[OECDrows,]

# uncomment this line to display only non-OECD countries
#data = data[!OECDrows,]

par(mfrow = c(1, 1))
plot(data[,"firearms"], data[,"homicides"], xlab="Firearms per 100", ylab="Homicides per 100,000")
text(data[,"firearms"], data[,"homicides"], data[,"country"], cex=0.6, col="#808080")
