import itertools
import math
import IPython
def partitions(nbox,extension=None,nrow=None,nmax=None):
    if nmax is None: nmax = nbox
    if nrow is None: nrow = nbox
    if extension is None: extension = [0]*nbox
    extension += [0]
    if nbox == 0: return None
    parts = []
    minval = max(0,int(math.ceil(float((sum(extension)+nbox))/nrow))-extension[0])
    maxval = min(nbox,nmax)
    for i in range(minval,maxval+1):
        rest = partitions(nbox-i,extension[1:],nrow-1,extension[0]+i-extension[1])
        parts += [[i]+x for x in rest] if rest is not None else [[i]]
    return parts

def fill(content,part):
    return [content[sum(part[:i]):sum(part[:i])+x] for i,x in enumerate(part)]
    
def diagram(part): 
    return [[None]*x for x in part]

def getfills(part):
    return [list(p) for p in itertools.permutations(sum([[i+1]*x for i,x in enumerate(part)],[]))]

def merge(a,b):
    return [x+y for x,y in itertools.izip_longest(a,b,fillvalue = [])]

def isstandard(tab):
    cols = [filter(lambda x:x is not None,c) for c in itertools.izip_longest(*tab)]
    return \
        all(all(col[i]<col[i+1] for i in range(len(col)-1)) for col in cols) and \
        all(all(row[i]<=row[i+1] for i in range(len(row)-1)) for row in tab)

def isrevlattice(tab):
    word = sum([[x for x in r if x is not None] for r in reversed(tab)],[])
    counts = [[len(filter(lambda z:z==v,word[x:])) for v in set(word)] for x in range(len(word))]
    return all(all(c[i]>=c[i+1] for i in range(len(c)-1)) for c in counts)

def dimension(part,n):
    distances = sum([[n+i-r for i in range(l)] for r,l in enumerate(part)],[])
    tr = [len([v-i for v in part if v-i > 0]) for i in range(max(part))]
    hooks  = [part[j]-i+tr[i]-j-1 for i,l in zip(range(part[0]),tr) for j in range(l)]
    return int(round(reduce(lambda x,y:x*y,[float(i)/j for i,j in zip(distances,hooks)])))

def decompose(first,second,n):
    tabs = []
    for f,p in itertools.product(getfills(second),partitions(sum(second),list(first),n)):
        a = merge(diagram(first),fill(f,p))
        if isstandard(a) and isrevlattice(a) and a not in tabs: tabs+=[a]
    return [[len(r) for r in t] for t in tabs]

def main():
    first  = [1,1]
    second = [1]
    
    print "{}x{}={}".format(dimension(first,3),dimension(second,3), "+".join([str(dimension(t,3)) for t in decompose(first,second,3)]))
        

if __name__ == '__main__':
    main()