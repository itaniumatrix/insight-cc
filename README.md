## Insight Twitter Graph Coding Challenge ReadMe
===========================================================

Kevin Wang
UC Berkeley
Materials Science & Engineering

## Required Packages

- Python 3.4+
- NetworkX (1.10)
[native to Python]
	-datetime
	-JSON
	-sys

Both features and Python scripts should be called with 2 arguments: 
-file_in 
-file_out

## Feature 1 (Cleaning Text): tweets_cleaned.py

This was done with native Python string operations.
tweets_cleaned.py

## Feature 2 (Graph of Hashtags, Compute Node Degrees): average_degree.py

The graph is built with NetworkX default implementation (regular Python dictionaries). For a large number of nodes and edges, a speed-up may be achieved by using a sorted dictionary, so we don't have to iterate through the whole graph to check against the timestamp.





