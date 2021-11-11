import os.path
import time
import tweepy
import json
import ctez_liq_collector


def update_tweeted_file(new_list):
    with open("tweeted.json", "w") as outfile:
        outfile.write(json.dumps(new_list))


def pick():
        liquidations = ctez_liq_collector.read_database()

        if not os.path.exists("tweeted.json"):
            with open("tweeted.json", "w") as tweet_file:
                tweet_file.write(json.dumps([]))

                print("created tweeted.json file")

        with open("tweeted.json", "r") as checkfile:
            checkdata = json.loads(checkfile.read())

        for op_hash in liquidations.keys():
            if op_hash in checkdata:
                print(f"Already tweeted {op_hash}")
            else:
                to_tweet = f"Oven belonging to https://tzkt.io/{liquidations[op_hash]['owner']} has been liquidated for {liquidations[op_hash]['xtz_lost']} $XTZ by https://tzkt.io/{liquidations[op_hash]['liquidator']} 🧨️"

                tweet(to_tweet)

                checkdata.append(op_hash)
                update_tweeted_file(checkdata)

                ban_prevention = 30
                print(f"Sleeping for {ban_prevention} seconds")


def tweet(what):
    print(f"Tweeting {what}")
    api_key, api_secret_key, access_token, access_token_secret = load_config()
    api = auth(api_key, api_secret_key, access_token, access_token_secret)
    api.update_status(what)
    print("Tweet sent")


def load_config():
    with open("config.json") as config_file:
        config = json.loads(config_file.read())

    api_key = config["api_key"]
    api_secret_key = config["api_secret_key"]
    access_token = config["access_token"]
    access_token_secret = config["access_token_secret"]
    return api_key, api_secret_key, access_token, access_token_secret


def auth(api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


if __name__ == "__main__":
    while True:
        try:
            pick()
            run_interval = 360
            print(f"Sleeping for {run_interval / 60} minutes")
            time.sleep(run_interval)
        except Exception as e:
            print(f"Error: {e}")

