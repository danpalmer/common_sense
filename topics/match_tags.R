# Get data
consultations = read.csv("consultation_tags.csv", header=T, stringsAsFactors=F)
twitter = read.csv("twitter_tags.csv", header=T, stringsAsFactors=F)

# Put into "dicts"
consultation_tags = list()
for (i in 1:nrow(consultations)) {
    consultation_tags[[i]] = gsub(" ", "", strsplit(consultations$tags[i], ",")[[1]])
}
twitter_tags = list()
for (i in 1:nrow(twitter)) {
    twitter_tags[[i]] = gsub(" ", "", strsplit(twitter$tags[i], ",")[[1]])
}

# Compare intersections of each user's tags against each consultation's tags
results = data.frame(matrix(nrow = length(twitter_tags), ncol = length(consultation_tags), data=NA))
colnames(results) = consultations$title
rownames(results) = twitter$title
for (i in 1:length(twitter_tags)) {
    for (j in 1:length(consultation_tags)) {
        results[i, j] = length(intersect(twitter_tags[[i]], consultation_tags[[j]]))
    }
}

# Print handy output
for (i in 1:length(twitter_tags)) {
    print(head(t(sort(results[i,], decreasing = T))))
}

# Identify why user X got tag Y
person = '@john_sandall'
person_loc = which(twitter$title == person)
winning_paper = colnames(results)[which(results[person_loc, ] == max(results[person_loc, ]))]
paper_loc = which(consultations$title == winning_paper)
intersect(twitter_tags[[person_loc]], consultation_tags[[paper_loc]])
