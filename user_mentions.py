import requests
import os
import json
from create_tweet_auto import main_post_reply
from loguru import logger
import time
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    user_id = 1563908807356456962
    return "https://api.twitter.com/2/users/{}/mentions".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserMentionsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    data = json_response['data']
    for mention in data:
        logger.info(mention)
        id = mention['id']
        text = mention['text']
        logger.info(id)
        logger.info(text)
        with open('mentions_replied_to.txt', 'r') as file:
            lines = file.read().splitlines()
            id_set = set(lines)
        if id in id_set:
            logger.info("Already replied to this tweet")
            continue
        response_code = main_post_reply(id, text)
        if response_code == 201:
            logger.info("Tweet posted successfully")
            with open('mentions_replied_to.txt', 'a') as file:
                file.write('\n')
                file.write(id)


if __name__ == "__main__":
    while True:
        logger.info("Running main")
        main()
        time.sleep(60)
