library(tm)

# Path to folder containing text files
dir_path = "./twitterati"
filenames = DirSource(dir_path)$filelist
filenames = gsub(dir_path, "", filenames)
filenames = gsub("/", "@", filenames)
filenames = gsub(".txt", "", filenames)

# Create corpus
doc.corpus = Corpus(DirSource(dir_path))
extendedstopwords = c("a","about","above","across","after","MIME Version","forwarded","again","against","all","almost","alone","along","already","also","although","always","am","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","aren't","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","below","best","better","between","big","both","but","by","c","came","can","cannot","can't","case","cases","certain","certainly","clear","clearly","come","could","couldn't","d","did","didn't","differ","different","differently","do","does","doesn't","doing","done","don't","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","her","here","here's","hers","herself","he's","high","higher","highest","him","himself","his","how","however","how's","i","i'd","if","i'll","i'm","important","in","interest","interested","interesting","interests","into","is","isn't","it","its","it's","itself","i've","j","just","k","keep","keeps","kind","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","let's","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","mustn't","my","myself","n","necessary","need","needed","needing","needs","never","new","newer","newest","next","no","nobody","non","noone","nor","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","ought","our","ours","ourselves","out","over","own","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","shan't","she","she'd","she'll","she's","should","shouldn't","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","such","sure","t","take","taken","than","that","that's","the","their","theirs","them","themselves","then","there","therefore","there's","these","they","they'd","they'll","they're","they've","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","wasn't","way","ways","we","we'd","well","we'll","wells","went","were","we're","weren't","we've","what","what's","when","when's","where","where's","whether","which","while","who","whole","whom","who's","whose","why","why's","will","with","within","without","won't","work","worked","working","works","would","wouldn't","x","y","year","years","yes","yet","you","you'd","you'll","young","younger","youngest","your","you're","yours","yourself","yourselves","you've","z")
control = list(
    stopwords = c(stopwords("english"), extendedstopwords),
    removePunctuation = TRUE,
    removeNumbers = TRUE,
    minDocFreq = 2,
    tolower = T,
    #stemming = T,
    wordLengths = c(3,Inf),
    weighting = weightTf
)
doc.tdm = TermDocumentMatrix(doc.corpus, control)
doc.tdm = removeSparseTerms(doc.tdm, 0.999)
doc.matrix = as.matrix(doc.tdm)

# Clean out some unpleasant unicode non-fun in a really stupid way
clean_string = function(x) {
    out = gsub("\001", "", x)
    remove_these = c(
        "\002", "\004l", "\004", "\035l", "\b", "\u0615", "\023", "\030", "\020",
        "\016", "\034", "\006", "\037", "\024", "\036", "\021", "\005", "\025",
        "\022", "\003", "\v", "\026", "\033", "\035", "\024")
    for (i in 1:length(remove_these)) {
        out = gsub(remove_these[i], "", out)
    }
    return(out)
}

rownames(doc.matrix) = clean_string(rownames(doc.matrix))

# Term counts, frequency, occurrence, density...
doc.counts = rowSums(doc.matrix) # how many docs is each word in?
# sort(doc.counts, decreasing=TRUE)[1:10] # top words
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

# doc.df[with(doc.df, order(-occurrence)), ]$term[1:30]
# doc.df[with(doc.df, order(-density)), ]$term[1:30]

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
    top.1000.words = read.csv("1000-words-csv.csv", header=F, stringsAsFactors=F, encoding="latin1")[,1]
    if (length(which(tags %in% top.1000.words)) > 0) {
        tags = tags[-which(tags %in% top.1000.words)]
    }
    tag_list = paste0(tags, collapse=", ")
    tag_df$tags[j] = tag_list
}

write.csv(tag_df, 'twitter_tags.csv')
