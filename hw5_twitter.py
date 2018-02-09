from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk
import ssl

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = "https://api.twitter.com/1.1/account/verify_credentials.json"
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth = auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3: Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1: Get Tweets
## set up the url and params for requesting data
baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {
    "screen_name": username,
    "count": num_tweets
    }
## request data
response = requests.get(baseurl, params = params, auth = auth) # request the data
results_lst = json.loads(response.text) # results_lst is a list of dictions (tweets)
results_dic = {} # create a diction to store the results_lst
results_dic["statuses"] = results_lst

## write the data in a file
results_file = "tweets.json" # file name: tweets.json
f = open(results_file, "w") # open the file
json_string = json.dumps(results_dic, indent = 2) # convert the python dic into a json string
f.write(json_string) # write the json string into the file
f.close() # close the file

#Code for Part 2: Analyze Tweets

## tokenize words in each tweet & get a frequency distribution
for tweet in results_dic["statuses"]:
    tokenized_text = nltk.word_tokenize(tweet["text"]) # tokenize the words in the tweet
    words_dic = nltk.FreqDist(tokenized_text) # get a frequency distribution of the tokenized list


real_words_lst = [] # create a list to store real words:
ignore_lst = ["http", "https", "RT"] # create a list of words that should be ignored

## go through each tweet & add real words to real_words_lst
for tweet in results_dic["statuses"]:
    tokenized_text = nltk.word_tokenize(tweet["text"]) # tokenize the words in the tweet

    # iterate through each word in tokenized_text & filter out the word if it's a stop word
    for word in tokenized_text:
        # check if the word starts with an alphabetic character [a-zA-Z]
        # check if the word is not in the ignore_lst
        if word[0].isalpha() and word not in ignore_lst:
            real_words_lst.append(word) # add the word to real_words_lst
        # else:
        #     print("Not a word: " + str(word))
        #     continue

## calcuate frequency distribution on real words
real_words_dic = nltk.FreqDist(real_words_lst)

## sort the words by their frequency
sorted_real_words_freq = sorted(real_words_dic.items(), key = lambda x: x[1], reverse = True)

## print the 5 most common words
print("THE 5 MOST FREQUENTLY USED WORDS:")
for word_freq_tuple in sorted_real_words_freq[0:5]:
    word, frequency = word_freq_tuple # unpack the tuple
    print(word, ":", frequency, "times")

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
