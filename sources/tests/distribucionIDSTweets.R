
ids = read.csv("ids.csv", header = FALSE)

plot(x = ids$V1, y = jitter(ids$V1))
