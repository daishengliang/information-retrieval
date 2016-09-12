# Mutual Information of Words.

## Introduction
Mutual information can be used to measure the correlation of two words.  We will use the CACM test collection to do some real computation, in which highly frequent words and very low frequent words have been removed (the vocabulary size of the original data is very large, so we won’t use it for this assignment). The CACM collection is a collection of titles and abstracts from the journal CACM. There are about 3,000 documents in the collection. The data set has been processed into lines. Each line contains one document, and the terms of each document are separated by blank space.

## Results
The output of function mutual_info.py is:

  The top 10 pairs with the highest mutual information.
  
  The top 5 words which have the highest mutual information with the word “programming” in the collection.

## How to run it?
Simply use python3 filename to run code.
  ```
  python3 mutual_info.py
  ```
