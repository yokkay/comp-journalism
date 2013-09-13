import sys
import csv
import string


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
    return a_string.split(" ")


def main():
    args = sys.argv[1:]

    if not args:
        print >> sys.stderr, "No args passed" 
        sys.exit(1)

    for arg in args:
        with open(arg, 'rb') as csv_file:
            reader = csv.reader(csv_file, quotechar='"')
            for row in reader:
                print row[0], row[1].split()[:2]


if __name__ == "__main__":
    main()
