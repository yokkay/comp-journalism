import sys
import config
from calais import Calais
import HTMLParser

def insert_link(start, end, doc, url):
    '''
    Creates hyperlink at string[start:] to string[:end]
    Indexes string by text not within angled brackets
    '''
    inside_tag = False
    max_i = 0
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

    #print start, end, true_start, true_end, doc[true_start:true_end],  "<br>"
    h = HTMLParser.HTMLParser()
    pre = str(h.unescape(doc[:true_start]))
    url = str(url)
    text = str(h.unescape(doc[true_start:true_end]))
    suff = str(h.unescape(doc[true_end:]))
    
    return "%s<a href=\"%s\">%s</a>%s" % (pre, url, text, suff)

def add_links(entities, doc_string):
    """ Add links to doc_string given entities list """
    total_offset = 0
    for entity in entities:
        if 'resolutions' in entity:
            url = entity['resolutions'][0]['id']
        else:
            url = "http://en.wikipedia.org/wiki/%s" % entity['name']
            url = url.replace(" ", "_")
        
        #print entity['name'], len(entity['instances']), '<br>'
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
    input = input.replace("<", "")
    input = input.replace(">", "")

    api_key = config.read_config('calais', 'api_key')
    calais = Calais(api_key, submitter="fridakahlo")
    entities = calais.analyze(input).entities
    
    #for e in entities: print e['name'], len(e['instances']), '<br>'

    linked_text = add_links(entities, input)
    for line in linked_text.splitlines():
        print "<p>", line, "<p>"

if __name__ == "__main__":
    main()
