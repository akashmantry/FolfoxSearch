# FolfoxSearch: Search Engine for wikipedia pages
This is as simple search engine I created which ranks using tf-idf and PageRank.

It consists of the following parts:

1. Crawled pages (set of 100 wikipedia pages) which were crawled using a crawler I created from scratch.
2. Parser, the crawled pages were parsed using various filtering techniques like stemming, stop word removeal, etc., discussed later.
3. Indexer, the crawled pages were indexed using a Cloudera VM running Hadoop MapReduce using python streaming.
4. Ranking, the pages were ranked using a combination of tf-idf and PageRank.
5. MongoDb, database to store parsed pages, indexing results, tf-idf results, etc.

## Parser
All the documents are in html and we need a parser to retreive meaningful information from them. BeautifulSoup and readability libraries were used to parse the raw html to get information. the results are stored in parsed_pages collection.

### Filtering
1. Lowercase the text so that we don't store same words multiple times.
2. Remove non-ascii words.
3. Remove punctuation and stop words.
4. Stem the words.

## Indexer
A simple map reduce script that maps words to their respective urls was run on a Cloudera VM. I used python streaming to run the scripts. The resultes are stored in indexer_model collection.

## Ranking
### Tf-Idf
1. To calculate term-frequency (tf), use the formula tf = n/N, where n = number of times the word appears in the document, and N = total number of words in the document. The results are stored in the tf collection.
2. To calculate inverse documnet frequency, use the formula idf = log(K/k+1), where K = total number of documents (in our case 100) and, k = the number of documents a term appears in. 1 is added in the denominator to eliminate division by 0. The results are stored in idf collection.
3. To calculate tf-idf, simply multiply the results of tf * idf for each term. The results are stored in tf-idf collection.

### Vectors
To calculate the vector, I used all the unique terms in the corpus. For each url, a vector is computed using the tf-idf values computed earlier. The results are stored in url_vector collection.

### PageRank
A simple PageRank algorithm is used to rank the pages. The algorithm uses the out_links file which was created while creawling. The file maps the url to all its out links. 

Combination of tf-idf and page rank is used to return the results. tf-idf is given more weigth than PageRank.

## Querying
1. Clean the query using the same filtering process.
2. Get the urls from the indexer collection depending on the terms in the query.
3. Calculate the vector (same sizing) of the query computing the tf-idf values.
4. Retrieve the page rank of each url.
5. Combine and output the sorted list of urls and combined ranking.

Test queries:

```
Aloyze Vanessa Laws
likvidacija prayer gugugug
Kansas assistance elected worship
ABSEES yokozuna
```


