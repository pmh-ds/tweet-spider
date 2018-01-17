import argparse
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main(hashtags, outfile):
    print("Starting headless Chrome browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)

    print("Building query URL...")
    base_url = u"https://twitter.com/search?q="
    query = "%20OR%20".join(u"%23" + hashtag for hashtag in hashtags)
    url = base_url + query

    print("Get URL...")
    browser.get(url)
    time.sleep(1)

    print("Find tweets...")
    body = browser.find_element_by_tag_name("body")

    for _ in range(50):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    tweet_elements = browser.find_elements_by_class_name("content")

    print("{} tweets found.".format(len(tweet_elements)))
    count = 1
    for tweet_element in tweet_elements:
        tweet = {}
        tweet["username"] = (tweet_element
                             .find_elements_by_class_name("stream-item-header")[0]
                             .find_elements_by_class_name("username")[0].text)
        tweet_text = tweet_element.find_elements_by_class_name("tweet-text")[0]
        tweet["text"] = tweet_text.text
        tweet["hashtag_mentions"] = [hashtag.text for hashtag in 
                                     tweet_text.find_elements_by_class_name("twitter-hashtag")]
        tweet["user_mentions"] = [user.text for user in
                                  tweet_text.find_elements_by_class_name("twitter-atreply")]
        tweet["timestamp"] =  int(tweet_element.find_elements_by_class_name("_timestamp")[0].get_attribute("data-time-ms"))
        tweet["link"] = tweet_element.find_elements_by_class_name("tweet-timestamp")[0].get_attribute("href")

        with open(outfile, "a") as f:
            f.write(json.dumps(tweet) + "\n")

        count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hashtags",
                        type=str,
                        nargs="+",
                        default=None,
                        help="Space delimited list of hashtag(s) to search.")
    parser.add_argument("--outfile",
                        type=str,
                        default="outfile.json",
                        help="Path to output file.")

    args = parser.parse_args()

    main(args.hashtags, args.outfile)
