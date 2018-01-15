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

tweets = browser.find_elements_by_class_name("tweet-text")

print("{} tweets found.\n".format(len(tweets)))
count = 1
for tweet in tweets:
    print("**** Tweet {} ****".format(count))
    print(tweet.text + "\n")
    count += 1
