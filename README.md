## Insight Twitter Graph: Coding Challenge
===========================================================
Kevin Wang

UC Berkeley

Materials Science & Engineering

## Required Packages

- Python 3.4+
- NetworkX (1.10)
- [native to Python]
 -- datetime
 -- JSON
 -- sys


## Feature 1 (Cleaning Text): 

Usage:
```tweets_cleaned.py filein fileout
```

This was performed with native Python string operations.

# Feature 2 (Graph of Hashtags, Compute Node Degrees): 

Usage: 
```average_degree.py filein fileout timewindow
```

--timewindow is the number of seconds window that the graph should contain, up until the most recently read Tweet. Default usage is 60s.

The graph is built with NetworkX default implementation (regular Python dictionaries). Speed is not great, because the program iterates through the entire list. An improved version of this would used a Sorted List of edges (by time), so you can stop the iteration once you reach nodes within the time window. This would achieve a speed up for a large number of nodes and high connectivity/degree in edges.

I began implementing a version overloading NetworkX with LastUpdatedOrderedDict rather than the regular dict. This works for Nodes, but the real issue lies in traversing the list of edges.



