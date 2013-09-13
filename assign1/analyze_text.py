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


def tf(tokens):
    """
    Returns dict of word counts (can use join later to merge into corpus dict)
    """
    counts = defaultdict(int)
    for token in tokens:
        counts[token] += 1
    return counts


def main():
    args = sys.argv[1:]

    if not args:
        print >> sys.stderr, "No args passed" 
        sys.exit(1)

    for arg in args:
        with open(arg, 'rb') as csv_file:
            csv.field_size_limit(sys.maxsize) # 'speech' field often larger than default field size limit
            reader = csv.reader(csv_file, quotechar='"')
            for row in reader:
                year = row[0]
                tokens = tokenize(row[1])
                counts = tf(tokens)


if __name__ == "__main__":
    main()
