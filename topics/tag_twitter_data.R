source('~/.tag_helpers.R')

db_conn = connect_to_db()
query = "SELECT * FROM consultations_consultation LIMIT 10"
results = dbFetch(dbSendQuery(db_conn, query), n = -1)


# Path to folder containing text files
dir_path = "./twitterati"
filenames = DirSource(dir_path)$filelist
filenames = gsub(dir_path, "", filenames)
filenames = gsub("/", "@", filenames)
filenames = gsub(".txt", "", filenames)


# Generate our TDM, convert to matrix
doc.tdm = get.tdm(d$text)
doc.matrix = as.matrix(doc.tdm)
rownames(doc.matrix) = clean_string(rownames(doc.matrix))


# Term counts, frequency, occurrence, density...
doc.counts = rowSums(doc.matrix) # how many docs is each word in?
doc.df = data.frame(
    cbind(names(doc.counts), as.numeric(doc.counts)),
    stringsAsFactors=FALSE)
names(doc.df) = c("term", "frequency")
doc.df$frequency = as.numeric(doc.df$frequency)
doc.occurrence = sapply(
    1:nrow(doc.matrix),
    function(i) {
        length(which(doc.matrix[i,] > 0)) / ncol(doc.matrix)
    }
)
doc.density = doc.df$frequency / sum(doc.df$frequency)
doc.df = transform(doc.df, density = doc.density, occurrence = doc.occurrence)


# Identify representative keywords for user
tag_df = data.frame(title = filenames, tags = NA)
for (j in 1:ncol(doc.matrix)) {
    print(j)
    doc = doc.matrix[, j]
    doc = doc[which(doc >= 2)]
    top_words = sort(doc, decreasing=T)
    top_df = data.frame(words = names(top_words), freq = as.numeric(top_words), avg_freq = NA, overindex = NA, occurrence = NA, density = NA, metric = NA)
    for (i in 1:length(top_words)) {
        this_word = names(top_words[i])
        this_freq = as.numeric(top_words[i])
        this_word.df = subset(doc.df, term == this_word)
        top_df$avg_freq[i] = this_word.df$frequency / (ncol(doc.matrix) * this_word.df$occurrence)
        top_df$overindex[i] = this_freq / top_df$avg_freq[i]
        top_df$occurrence[i] = this_word.df$occurrence
        top_df$density[i] = this_word.df$density
        top_df$metric[i] = top_df$overindex[i] / top_df$occurrence[i]
    }    
    top_df = top_df[order(top_df$metric, decreasing=T),]
    top_df = subset(top_df, metric >= 2)
    tags = as.character(top_df$words)
    if (length(which(tags %in% top.1000.words)) > 0) {
        tags = tags[-which(tags %in% top.1000.words)]
    }
    tag_list = paste0(tags, collapse=", ")
    tag_df$tags[j] = tag_list
}

write.csv(tag_df, 'twitter_tags.csv')
