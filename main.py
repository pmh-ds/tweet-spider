import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

print("Starting headless Chrome browser...")
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=options)

print("Building query URL...")
base_url = u"https://twitter.com/search?q="
query = u"%23bitcoin"
url = base_url + query

print("Get URL...")
browser.get(url)
time.sleep(1)

print("Find tweets...")
body = browser.find_element_by_tag_name("body")

for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

tweet_elements = browser.find_elements_by_class_name("content")

print("{} tweets found.\n".format(len(tweet_elements)))
count = 1
tweets = []
for tweet_element in tweet_elements:
    print("**** Tweet {} ****".format(count))
    tweet = {}
    tweet["username"] = (tweet_element
                         .find_elements_by_class_name("stream-item-header")[0]
                         .find_elements_by_class_name("username")[0].text)
    tweet["text"] = tweet_element.find_elements_by_class_name("tweet-text")[0].text
    tweet["timestamp"] =  int(tweet_element.find_elements_by_class_name("_timestamp")[0].get_attribute("data-time-ms"))
    print(tweet)
    print("\n")
    count += 1
