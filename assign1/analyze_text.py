import sys
import csv
import string
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
    def idf(term): return log(num_docs/df_count[term])
    def tf(term): return tf_count[term]

    # TODO: create tfidf vector for document
    # maintain ordering from df_count

def main():
    args = sys.argv[1:]

    if not args:
        print >> sys.stderr, "No args passed" 
        sys.exit(1)

    for arg in args:
        with open(arg, 'rb') as csv_file:
            csv.field_size_limit(sys.maxsize) # 'speech' field often larger than default field size limit
            reader = csv.reader(csv_file, quotechar='"')

            years = []
            all_tf_counts = []
            df_count = defaultdict(int) # maps term to number of documents term appears in

            for row in reader:
                years.append(row[0])
                tokens = tokenize(row[1])
                tf_count, df_count = count(tokens, df_count)
                all_tf_counts.append(tf_count)

            tfidf_vectors = []
            for tf_count in all_tf_counts:
                vector = tfidf(len(years), tf_count, df_count)
                tfidf_vectors.append(vector)

if __name__ == "__main__":
    main()
