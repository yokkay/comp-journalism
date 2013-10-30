import sys
import random

args = sys.argv[1:]

if not args:
    print "No args"
    sys.exit(1)

n = sys.argv[1]

try: 
    n = int(n)
except:
    print "%s not an int" % n
    sys.exit(1)

print "\n".join([str(i) for i in random.sample(xrange(n), 5)])
