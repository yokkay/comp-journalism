data = read.csv("firearms.csv", header=T, sep=",")

# plot all OECD countries except the US and mexico
keeprows = data[,"OECD"]=="Y"
keeprows = keeprows & !(data[,"country"] == "United States") & !(data[,"country"] == "Mexico")
data = data[keeprows,]

# create a matrix with as many rows as countries, plus 9 columns
charts = matrix(numeric(0), dim(data)[1], 9)

# this chart will be the one with the real data
realchart = sample(1:9, 1)

# fake data for testing, perfect correlation
# COMMENT these lines ONLY when your randomization works and you are ready to run the test
data[,"firearms"] = seq(1:dim(data)[1])
data[,"homicides"] = seq(1:dim(data)[1])

# Fill columns of charts matrix with random permutations of realdata, except for realchart
# hints:
#   the y values are data[, "homicides"]
#   to set column i of charts, use charts[,i]=...

# YOUR CODE GOES HERE 


# Now plot the charts in a grid
par(mfrow = c(3, 3))
for (i in 1:9) {
	plot(data[,"firearms"], charts[,i], xlab="", ylab="")
}

cat("Press enter to reveal real chart\n")
readline()
cat("Real data is in chart number ", realchart, "\n")
