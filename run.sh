#!/usr/bin/env bash

# Shell script to call the two Python3 scripts

# Looks nearly identical to the example shell script (but I wrote my program and shell script before seeing that) -> We have similar coding styles!
# average_degree.py takes a 3rd argument: time_window, the number of seconds

python3 ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
python3 ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt 60



