source('./tag_helpers.R')

db_url = Sys.getenv('DATABASE_URL')
db_conn = connect_to_db(db_url)
query = "SELECT id, title, summary, organisation, raw_text FROM consultations_consultation"
results = dbFetch(dbSendQuery(db_conn, query), n = -1)

# Read in the data, concatenate all text fields into one; cleaning
results$text = paste0(results$title, " ", results$summary, " ", results$organisation, " ", results$raw_text)
results$text = gsub('\f', '', results$text)

# Generate our TDM, convert to matrix
doc.tdm = get.tdm(results$text)
doc.matrix = as.matrix(doc.tdm)
rownames(doc.matrix) = clean_string(rownames(doc.matrix))

# Construct df with terms, frequencies, occurrences (i.e. unique documents containing each term)
doc.counts = rowSums(doc.matrix) # how many docs is each word in?
doc.df = data.frame(
    cbind(names(doc.counts), as.numeric(doc.counts)),
    stringsAsFactors=FALSE)
names(doc.df) = c("term", "frequency")
doc.df$frequency = as.numeric(doc.df$frequency)
doc.occurrence = sapply(
    1:nrow(doc.matrix),
    function(i) length(which(doc.matrix[i,] > 0)) / ncol(doc.matrix)
)

# Add density (i.e. frequency divided by total words in corpus)
doc.density = doc.df$frequency / sum(doc.df$frequency)
doc.df = transform(doc.df, density = doc.density, occurrence = doc.occurrence)


# Generate a list of representative keywords for each document
# i.e. what does document X contain that are unique to it, or it overindexes on?
tag_df = data.frame(consultation_id = results$id, tags = NA)
for (j in 1:ncol(doc.matrix)) {  # Iterating over documents
    doc = doc.matrix[, j]
    doc = doc[which(doc >= 2)]  # Eliminate terms that only occur once in this doc
    top_words = sort(doc, decreasing=T)
    top_df = data.frame(
        words = names(top_words),
        freq = as.numeric(top_words),
        avg_freq = NA,
        overindex = NA,
        occurrence = NA,
        density = NA,
        metric = NA
    )
    # Iterate over each term in the doc, calculate several metrics
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
    # The "metric" is where the magic happens
    top_df = top_df[order(top_df$metric, decreasing=T),]
    # Filter down our list of tags to only the most representative keywords
    if (nrow(top_df) >= 10) {
        top_df = subset(top_df, metric >= 2)
    }
    if (nrow(top_df) >= 10) {
        top_df = subset(top_df, freq >= 4)
    }
    # If we still have loads, take the top 10 by "metric" and top 10 by overindexing
    if (nrow(top_df) >= 20) {
        top_df = rbind(
            top_df[1:10, ],
            top_df[order(top_df$overindex, decreasing=T), ][1:10, ]
        )
    }
    # Construct list of tags, remove any that are common words
    tags = as.character(top_df$words)
    if (length(which(tags %in% top.1000.words)) > 0) {
        tags = tags[-which(tags %in% top.1000.words)]
    }
    tag_list = paste0(tags, collapse=", ")
    tag_df$tags[j] = tag_list
}

out = write.table(tag_df, sep=",", row.names=F)
