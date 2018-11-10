import argparse
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


BASE_URL = u"https://twitter.com/search?q="


def build_url(hashtags, base_url=BASE_URL):
    """Build URL to query hashtags."""
    query = "%20OR%20".join(u"%23" + hashtag for hashtag in hashtags)
    return base_url + query


def find_tweets(browser, url, num_scrolls=50):
    """Get URL and find tweets."""
    logging.info("Get URL...")
    browser.get(url)
    time.sleep(1)

    logging.info("Find tweets...")
    body = browser.find_element_by_tag_name("body")

    for _ in range(num_scrolls):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    return browser.find_elements_by_class_name("content")


def parse_tweet(tweet_element):
    """Parse tweet element."""
    tweet = {}

    tweet["username"] = tweet_element \
        .find_elements_by_class_name("stream-item-header")[0] \
        .find_elements_by_class_name("username")[0].text

    tweet_text = tweet_element.find_elements_by_class_name("tweet-text")[0]

    tweet["text"] = tweet_text.text

    tweet["hashtag_mentions"] = [
        hashtag.text for hashtag in
        tweet_text.find_elements_by_class_name("twitter-hashtag")
    ]

    tweet["user_mentions"] = [
        user.text for user in
        tweet_text.find_elements_by_class_name("twitter-atreply")
    ]

    tweet["timestamp"] = \
        int(tweet_element.find_elements_by_class_name("_timestamp")[0]
            .get_attribute("data-time-ms"))

    tweet["link"] = \
        tweet_element.find_elements_by_class_name("tweet-timestamp")[0] \
        .get_attribute("href")

    return tweet


def main(hashtags, out_file, num_scrolls):
    """Run spider."""
    logging.info("Starting headless Chrome browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)

    logging.info("Building query URL...")
    url = build_url(hashtags)

    tweet_elements = find_tweets(browser, url, num_scrolls)

    logging.info("{} tweets found.".format(len(tweet_elements)))

    logging.info("Parse tweets...")
    for tweet_element in tweet_elements:

        tweet = parse_tweet(tweet_element)

        with open(out_file, "a") as f:
            f.write(json.dumps(tweet) + "\n")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--hashtags",
                        type=str,
                        nargs="+",
                        default=None,
                        help="Space delimited list of hashtag(s) to search.")
    parser.add_argument("--out_file",
                        type=str,
                        default="out_file.json",
                        help="Path to output file.")
    parser.add_argument("--num_scrolls",
                        type=int,
                        default=50,
                        help="Number of times the spider will scroll.")

    args = parser.parse_args()

    main(args.hashtags, args.out_file, args.num_scrolls)
