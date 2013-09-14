import sys
import csv
import string
from math import *
from collections import defaultdict

def tokenize(a_string):
    """
    Tokenize string per scheme: 
    (1) convert all chars to lowercase
    (2) remove all punctuation
    (3) split on space
    """

    a_string = a_string.lower()
    table = string.maketrans("","")
    a_string = a_string.translate(table, string.punctuation)
    return a_string.split() # splitting on whitespace, not space char


def count(tokens, df_counts):
    """
    Returns dict of word counts (can use join later to merge into corpus dict)
    """
    tf_counts = defaultdict(int)
    for token in tokens:
        tf_counts[token] += 1
    for term in tf_counts:
        df_counts[term] += 1
    return tf_counts, df_counts


def tfidf(num_docs, tf_count, df_count):
    """
    Returns "vector" (defaultdict) of tfidf weights which sum to 1
    """
    def idf(term): return log(num_docs/df_count[term])
    def tf(term): return tf_count[term]

    vector = defaultdict(float) # note this is not a list
    for term in df_count:
        tfidf = tf(term) * idf(term)
        vector[term] = tfidf

    total = sum(vector.values())
    for term in vector:
        vector[term] = vector[term]/total # make sure vector sums to 1

    return vector


def main():
    args = sys.argv[1:]

    if not args:
        print >> sys.stderr, "No args passed" 
        sys.exit(1)

    for arg in args:
        with open(arg, 'rb') as csv_file:
            csv.field_size_limit(sys.maxsize) # 'speech' field often larger than default field size limit
            reader = csv.reader(csv_file, quotechar='"')

            all_tf_counts = {}
            df_count = defaultdict(int) # maps term to number of documents term appears in

            for row in reader:
                year = row[0]
                tokens = tokenize(row[1])
                tf_count, df_count = count(tokens, df_count)
                all_tf_counts[year] = tf_count

            tfidf_vectors = {}
            for year in all_tf_counts:
                tf_count = all_tf_counts[year]
                vector = tfidf(len(years), tf_count, df_count)
                tfidf_vectors[year] = vector
            
            


if __name__ == "__main__":
    main()
