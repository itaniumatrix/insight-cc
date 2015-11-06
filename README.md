## Insight Twitter Graph Coding Challenge ReadMe
===========================================================

Kevin Wang
UC Berkeley

Materials Science & Engineering

## Required Packages

- Python 3.4+
- NetworkX (1.10)
-[native to Python]
 -datetime
 -JSON
 -sys


# Feature 1 (Cleaning Text): 

Usage:
'''tweets_cleaned.py filein fileout
'''

This was performed with native Python string operations.

# Feature 2 (Graph of Hashtags, Compute Node Degrees): 

Usage: 
'''average_degree.py filein fileout timewindow
'''

--timewindow is the number of seconds window that the graph should contain, up until the most recently read Tweet. Default usage is 60s.

The graph is built with NetworkX default implementation (regular Python dictionaries). For a large number of nodes and edges, a speed-up may be achieved by using a sorted dictionary, so we don't have to iterate through the whole graph to check against the timestamp. Using a sorted dictionary also incurs a cost





