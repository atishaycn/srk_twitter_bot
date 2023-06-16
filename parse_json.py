import ast
import os
import requests
from loguru import logger
import time

bearer_token = os.environ.get("BEARER_TOKEN")

print(bearer_token)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def get_tweet_from_id(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    while True:
        response = requests.request("GET", url, auth=bearer_oauth)
        logger.info(response.status_code)
        if response.status_code == 429:
            logger.info("Too Many Requests, waiting for 30 seconds...")
            for i in range(30, 0, -1):
                # Overwrite the current line with the countdown
                print(i, end='\r')
                logger.info(i)
                time.sleep(1)  #
        elif response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        else:
            break  # Exit loop if status code is 200
    return response.json()['data']['text']


def format_referenced_tweets(content, i):
    data = ast.literal_eval(content)
    all_tweets = ""
    full_tweet = ""
    for tweet in data['data']:
        current_tweet = tweet['text']
        logger.info(current_tweet)
        with open('output_file_append.txt', 'r') as file:
            already_proccessed = file.read()
        logger.info("check if already proccessed")
        if current_tweet in already_proccessed:
            logger.info("already proccessed")
            continue
        logger.info("not proccessed")
        if 'referenced_tweets' in tweet:
            logger.info("found refrence tweet")
            responded_to_tweet = get_tweet_from_id(
                tweet['referenced_tweets'][0]['id'])
            responded_to_tweet = responded_to_tweet.replace('\n', ' ')
            all_tweets += "fan's tweet: " + responded_to_tweet + "\n"
            full_tweet += "fan's tweet: " + responded_to_tweet + "\n"
            all_tweets += "srk's reply: " + tweet['text'] + "\n"
            full_tweet += "srk's reply: " + tweet['text'] + "\n"
            logger.info(responded_to_tweet)
            with open('output_file_append.txt', 'a') as file:
                file.write(all_tweets)
            all_tweets = ""
    output_file = "all_tweets_{}.txt".format(i)
    with open(output_file, 'w') as file:
        file.write(full_tweet)


def main():
    i = 0
    while i < 9:
        file_name = "json_file_{}.txt".format(i)
        logger.info("Reading from file: {}".format(file_name))
        with open(file_name, 'r') as file:
            content = file.read()
            format_referenced_tweets(content, i)
        i += 1
        if not content:
            break


if __name__ == "__main__":
    main()
