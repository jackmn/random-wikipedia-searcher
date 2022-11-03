# random-wikipedia-searcher

#Usage

The python file should run as standard in any python environment. The user will be prompted to write there search term after runnning the file and a list of the most relevant articles pulled will be returned to the user in order of relevancy. The function used to pull these articles is random so the same results will not occur for multiple search requests.

The test file can be run as long as the files are all downloaded in the folder and then the command "python -m unittest {file location}" is run. A search query is still required due to the way the test file is calling the wiki searcher. The test file will return the number of tests, the time taken, and if they were successful.




#Improvements
1. Speed optimisation - This is a very unoptimised piece of code due to the short time to work on it. There are a number of ways this could be optimised further the first would be not doing any cleaning on the code which will be discussed further down. A second is changing the search area so that so that the whole text is not taken into account as it is likely most of the correnlation could be done with just the title and the first paragraph of the text. As well as these tf-idf can become slow with large vocabulary as would be expected in these datasets.
2. Graphical Solution - A graphical solution could be implemented in two different ways, one way is to link the words being searched to familiar words with a large dataset which would assist in the searching accuracy rather than just searching for the specific instances of the word as is done in this case. The second way a graphical solution could be beneficial is to combine elements of the articles together with a pool of relevant words. This might have a high computational requirement but could be done at any time rather than just when a call is made and that would make it much more efficient for future users searching using the graph as a reference point.
3. Data Cleaning - I would have liked to included the section of the code that is commmented that would remove common words in the text but there was an issue in the h tags where all of these values were being removed as there are a lot of common words here and that was leading to errors in the vectorizer which I didn't have the time to fully debug. On top of this the cleaning may have been, at least to some extent, not that useful as there is not much information gained from removing these and it just takes computational time.
4. Further Linking - The current solution searches by each word individually and while this will come to an adequate solution it doesn't account for word groupings. These could be added to look for phrases that could have a stronger correlation to the initial query over instances where the words appear out of order.
