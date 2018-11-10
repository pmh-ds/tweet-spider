# Tweet Spider
A simple spider for collecting tweets containing specified hashtags.

## Installation
Clone the repository and move into the directory.

```
git clone https://github.com/smoothml/tweet-spider.git && cd tweet-spider
```

Install the Python requirements. You will probably want to use a virtual environment, in which case, assuming you have Python 3 installed, run the following

```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

You also need to install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home). On macOS you can do this with

```
brew tap homebrew/cask
brew cask install chromedriver
```

## Usage
One everything is installed you can start collecting tweets. To query the hashtags #socks, for example, and store the output to socks.json, run

```
python main.py --hashtags socks --out_file socks.json
```

If you want to search for multiple hashtags, supply them to the `--hashtags` argument as a space-delimited list, for example

```
python main.py --hashtags socks shoes hats --out_file socks_shoes_hats.json
```

If you want to find more tweets supply the `--num_scrolls` argument with an integer, for example

```
python main.py --hashtags socks shoes hats --out_file socks_shoes_hats.json --num_scrolls 500
```

Twitter loads as you scroll so by telling the spider to scroll more you will collect more tweets. The default value if 50.
