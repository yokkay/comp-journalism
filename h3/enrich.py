import sys
import config
from calais import Calais
import HTMLParser

def insert_link(start, end, doc, url):
    '''
    Creates hyperlink at string[start:] to string[:end]
    Indexes string by text not within angled brackets
    '''
    inside_tag = None
    i, true_start, true_end = 0, 0, 0
    for j, ch in enumerate(doc):
        if ch == '<':
            inside_tag = True
        elif ch == '>':
            inside_tag = False
        elif not inside_tag:
            if i == start:
                true_start = j
            elif i == end:
                true_end = j
            i += 1

    h = HTMLParser.HTMLParser()
    s = str(h.unescape(doc[:true_start]))
    t = str(url)
    u = str(h.unescape(doc[true_start:true_end]))
    v = str(h.unescape(doc[true_end:]))
    
    return "%s<a href=\"%s\">%s</a>%s" % (s, t, u, v)

def add_links(entities, doc_string):
    """ Add links to doc_string given entities list """
    total_offset = 0
    for entity in entities:
        if 'resolutions' in entity:
            url = entity['resolutions'][0]['id']
        else:
            url = "http://en.wikipedia.org/wiki/%s" % entity['name']
            url = url.replace(" ", "_")
        
        for instance in entity['instances']:
            offset = instance['offset']
            length = instance['length']
            doc_string = insert_link(offset, offset+length, doc_string, url)

    return doc_string


def usage():
    """ Prints usage information """
    print "Usage: python enrich.py"
    print "Reads from stdin and prints to stdout"


def main():
    """ Main method """

    if not sys.stdin:
        usage()
        sys.exit(1)

    input = sys.stdin.read() # read from stdin

    api_key = config.read_config('calais', 'api_key')
    calais = Calais(api_key, submitter="fridakahlo")
    entities = calais.analyze(input).entities
    
    #for e in entities: print e['name'], len(e['instances']), '<br>'

    linked_text = add_links(entities, input)
    for line in linked_text.split("\n"):
        print line, "<br>",


if __name__ == "__main__":
    main()
