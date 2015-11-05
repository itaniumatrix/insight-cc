Insight Data Engineering - Coding Challenge
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

1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

Here, we have to define a few concepts (though there will be examples below to clarify):

- A tweet's text is considered "clean" once all of the escape characters (e.g. \n, \", \/ ) and unicode have been removed.
- A Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet.

## Details of Implementation

We'd like you to implement your own version of these two features.  However, we don't want this challenge to focus on the relatively uninteresting "dev ops" of connecting to the Twitter API, which can be complicated for some users.  Normally, tweets can be obtained through Twitter's API in JSON format, but you may assume that this has already been done and written to a file named `tweets.txt` inside a directory named `tweet_input`.  For simplicity, this file `tweets.txt` will only contain the actual JSON messages (in reality, the API also can emit messages about the connection and the API rate limits).  Additionally, `tweets.txt` will have the content of each tweet on a newline:

tweets.txt:

	{JSON of first tweet}  
	{JSON of second tweet}  

## First Feature

The point of the first feature is to extract and clean the relevant data for the Twitter JSON messages.  For example, a typical tweet might come in the following JSON message (which we have expanded on to multiple lines to make it easier to read):
