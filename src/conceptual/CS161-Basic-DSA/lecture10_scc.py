# -*- coding: utf-8 -*-
"""lecture10_scc.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/stanford-cs161/winter2025-extra/blob/colab/lecture10_scc.ipynb

**Attribution:** These notebooks were originally developed by Mary Wotters and have possibly been modified by Nima Anari and Moses Charikar. Please direct any concerns to Nima and Moses.
"""

# This part downloads needed auxiliary files to Google Colab
! curl https://stanford-cs161.github.io/winter2025-extra/lecture10_scc-aux.zip > lecture10_scc-aux.zip && unzip -o lecture10_scc-aux.zip

"""# Lecture 10: SCC's"""

from graphStuff import *

"""### Test graph:

Here's the graph that is the running example on the slides
"""

stanford = CS161Vertex("Stanford")
wiki = CS161Vertex("Wikipedia")
nytimes = CS161Vertex("NYTimes")
cal = CS161Vertex("Berkeley")
puppies = CS161Vertex("Puppies")
google = CS161Vertex("Google")

G = CS161Graph()
V = [ stanford, wiki, nytimes, cal, puppies, google ]
for v in V:
    G.addVertex(v)
E = [ (stanford, wiki), (stanford, puppies), (wiki, stanford), (wiki, nytimes), (nytimes, stanford), (cal, stanford), (cal, puppies), (wiki,puppies), (nytimes, puppies), (puppies, google), (google, puppies) ]
for x,y in E:
    G.addDiEdge( x,y )

print(G)

"""## Now let's implement our SCC algorithm.

We'll need to modify the DFS code we had from last time
"""

def DFS_helper( w, currentTime, ordering, verbose ):
    if verbose:
        print("Time", currentTime, ":\t entering", w)
    w.inTime = currentTime
    currentTime += 1
    w.status = "inprogress"
    for v in w.getOutNeighbors():
        if v.status == "unvisited":
            currentTime = DFS_helper(v, currentTime, ordering, verbose)
            currentTime += 1
    w.outTime = currentTime
    w.status = "done"
    ordering.insert(0, w)
    if verbose:
        print("Time", currentTime, ":\t leaving", w)
    return currentTime

# This is a version of DFS which outputs vertices in the order that DFS leaves them.
# We used it for topological sorting in Lecture 9
def SCC( G, verbose=False ):
    ordering = []
    for v in G.vertices:
        v.status = "unvisited"
        v.inTime = None
        v.outTime = None
    currentTime = 0
    for w in G.vertices:
        if w.status == "unvisited":
            currentTime = DFS_helper( w, currentTime, ordering, verbose )
        currentTime += 1
    # now reverse all the edges
    E = G.getDirEdges()
    for x,y in E:
        G.reverseEdge(x,y)

    # and do it again, but this time in the order "ordering"
    SCCs = []
    for v in ordering:
        v.status = "unvisited"
        v.inTime = None
        v.outTime = None
    currentTime = 0
    for w in ordering:
        visited = []
        if w.status == "unvisited":
            currentTime = DFS_helper( w, currentTime, visited, verbose )
            SCCs.append(visited[:])
        currentTime += 1
    return SCCs

"""### The moment of truth...

Does this algorithm work?
"""

print(G)

SCCs = SCC(G, False)
for X in SCCs:
    print ([str(x) for x in X])

"""## It does!  But why?"""

