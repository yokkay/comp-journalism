from math import *
from collections import defaultdict
import sys
import csv
import string
import json


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


def usage():
    print >> sys.stderr, "Usage:"
    print >> sys.stderr, "python analyze_text.py TFIDF [csv] > [json]"
    print >> sys.stderr, "python analyze_text.py TOP-YEAR [year] [TFIDF json output]"
    print >> sys.stderr, "python analyze_text.py TOP-DECADE [year beginning decade] [TFIDF json output]"


def main():
    args = sys.argv[1:]

    if not args:
        print >> sys.stderr, "Error: No args passed" 
        usage()
        sys.exit(1)

    mode = args[0]
    args = args[1:]

    if mode == 'TFIDF':
        with open(args[0], 'rb') as csv_file:
            csv.field_size_limit(sys.maxsize) # 'speech' field often larger than default field size limit
            reader = csv.reader(csv_file, quotechar='"')

            num_docs = 0
            all_tf_counts = {}
            df_count = defaultdict(int) # maps term to number of documents term appears in

            for row in reader:
                # TODO: Remembered years aren't unique identifier... must change index
                num_docs += 1
                year = row[0]
                tokens = tokenize(row[1])
                tf_count, df_count = count(tokens, df_count)
                all_tf_counts[year] = tf_count

            tfidf_vectors = {}
            for year in all_tf_counts:
                print >> sys.stderr, "Computing tfidf for year %s" % year
                tf_count = all_tf_counts[year]
                vector = tfidf(num_docs, tf_count, df_count)
                tfidf_vectors[year] = vector
            
            print json.dumps(tfidf_vectors)

    elif mode == 'TOP-YEAR':
        year = args[0]
        print >> sys.stderr, "Loading json from %s..." % args[1]
        tfidf_vectors = json.load(open(args[1], 'rb'))
        print >> sys.stderr, "Loaded json, now getting top 20 in year %s" % year
        if year in tfidf_vectors:
            vector = tfidf_vectors[year]
            top_20 = sorted(vector, key=vector.get, reverse=True)[:20]
            for term in top_20:
                print "%s %f" % (term, vector[term])
        else:
            print >> sys.stderr, "Error: %s not in json %s" % (year, args[1])

    elif mode == 'TOP-DECADE':
        year = int(args[0])
        years = [year + i for i in range(0,10)]        

    else:
        print >> sys.stderr, "Error: %s not valid mode" % mode
        usage()


if __name__ == "__main__":
    main()
