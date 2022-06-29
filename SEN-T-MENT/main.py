from unittest import result
import tweepy
from flask import Flask, render_template, redirect, url_for, request,jsonify
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import json
import re
import csv
name1 ="HackSa"
app = Flask(__name__)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

    

def get_tweets(api, query, count=5):
    count = int(count)
    tweets = []
    try:

        fetched_tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(count)
        count_pos = 0
        count_neg = 0
        count_neu = 0
        dictionary = {}
        for tweet in fetched_tweets:

            parsed_tweet = {}

            if 'retweeted_status' in dir(tweet):
                parsed_tweet['text'] = tweet.retweeted_status.full_text
            else:
                parsed_tweet['text'] = tweet.full_text

            parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text'])
            # count positive, negative and neutral tweets
            if parsed_tweet['sentiment'] == 'positive':
                count_pos += 1
            elif parsed_tweet['sentiment'] == 'negative':
                count_neg += 1
            elif parsed_tweet['sentiment'] == 'neutral':
                count_neu += 1
                

           
            

            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        dictionary['tweet'] = tweets
        dictionary['count_pos'] = count_pos
        dictionary['count_neg'] = count_neg
        dictionary['count_neu'] = count_neu        
        #print(tweets)
        print("Positive:",count_pos)
        print("Negative",count_neg)
        print("Neutral",count_neu)
        return dictionary
    except tweepy.TweepyException as e:
        print("Error : " + str(e))

@app.route('/')
def disp():
    return render_template('main.html')


@app.route("/pred", methods=['POST', 'GET'])
def pred():
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        count = request.form['num']
        print(count)
        fetched_tweets = get_tweets(api, query, count)
        result = fetched_tweets
        print(result)
        return render_template('result.html', result=result)
        
    



        

if __name__ == '__main__':
    consumer_key = "2wNx3WUNBJFr9dxc5f5KEwlEp"
    consumer_secret = "UjCi5Ja59brWdYQYqDXdnthc40uY5FLpNCOH3SF3Jf3YDd5wkt"
    access_token = "1518987443650789376-l77cehtyDf8DTnzx1jB5BUSxPnaB13"
    access_token_secret = "8dmILbjI3jQmutIsdVJ634qn85MIQ8iu3lbStasBZGWk4"

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    app.debug = True
    app.run(host='localhost')


