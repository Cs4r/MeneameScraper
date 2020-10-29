#!/usr/bin/python3
import argparse
import time
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import os
from meneameGraphicsManager import MeneameGraphicsManager

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

class CustomArgParser(argparse.ArgumentParser):
    """
    Class overriden
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def epoch_to_formatted_date(epoch):
    """
    Converts the timestamp to formated date
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))


def string_to_date(date):
    """
    Converts string date to formated date
    """
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def handle_separator(text):
    """
    Replaces all charaters ; by an empty character in the given text
    """
    separator = ";"
    if type(text) == str:
        return text.replace(separator, "")
    else:
        raise TypeError("Only strings can be handled")


def scrap(url):
    """
    Method used to scrap each of the news given in the URL passed as parameter
    """
    #performs the request to the given URL
    page = requests.get(url, headers=HEADERS)
    #creates a BeautifulSoup object with the html content obtained from the request
    soup = BeautifulSoup(page.content, features="html.parser")
    news = dict()

    news["title"] = handle_separator(soup.title.text)

    news["paragraph"] = handle_separator(soup.find(class_="news-content").text)

    tags = []
    for link in soup.select(".news-tags a"):
        tags.append(link.text.strip())
    #array joined in a single string
    tags_joined = ','.join(tags)
    news["tags"] = tags_joined

    news["votes"] = int(soup.select(".votes a")[0].text)

    news["down-votes"] = int(soup.select(".negative-vote-number")[0].text)

    news["clicks"] = int(
        soup.select("#newswrap > div.news-summary > div > div.news-shakeit.mnm-published > div.clics > span")[0].text)

    news["comments"] = int(soup.select(".news-details-main > .comments")[0].text.replace("comentarios", ""))

    news["sent-date"] = epoch_to_formatted_date(int(soup.select(".ts.visible")[0].attrs['data-ts']))

    news["pub-date"] = epoch_to_formatted_date(int(soup.select(".ts.visible")[1].attrs['data-ts']))

    news["category"] = soup.select(".tool.sub-name > .subname")[0].text

    news["karma"] = int(soup.select(".karma-number")[0].text)

    news["source"] = soup.select("#newswrap > div.news-summary > div > div.center-content > div.news-submitted > "
                                 "span.showmytitle")[0].text

    return news


def list_news_until_date(stop_date):
    """
    Method that lists the URLs of the news from Meneame.net
    until the date given as parameter
    """
    page_number = 1
    list_of_urls = []
    fetch_news = True

    while fetch_news:
        #starting from page 1, start scraping each page looking for the latests
        #news given the stop date
        url = "https://www.meneame.net/?page=" + str(page_number)
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="html.parser")

        for comment in soup.select(".comments"):
            # Ignore articles since they haven't got interesting content
            if comment.parent.parent.select(".subname") != [] \
                    and comment.parent.parent.select(".subname")[0].text == "Artículos":
                continue

            attrs = comment.attrs
            if attrs["class"] == ["comments"]:
                news_pub_date_str = epoch_to_formatted_date(
                    int(comment.parent.parent.parent.select(".ts.visible")[1].attrs["data-ts"]))

                print(news_pub_date_str)

                news_pub_date = string_to_date(news_pub_date_str)

                if stop_date > news_pub_date:
                    print("%s > %s" % (stop_date, news_pub_date))
                    fetch_news = False
                    break

                relative_url = attrs["href"]
                full_url = "https://www.meneame.net" + relative_url
                list_of_urls.append(full_url)

        page_number = page_number + 1

    return list_of_urls


if __name__ == '__main__':

    path = './csv/dataset.csv'
    #argument definition to be used 
    parser = CustomArgParser()
    parser.add_argument("-g","--show_graphs", help="show graphs of the dataset", action='store_true')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-sd","--stop_date", help="date to stop fetching news")
    args = parser.parse_args()

    #if argument stop date provided
    if args.stop_date is not None:
        stop_date = datetime.strptime(args.stop_date, "%d/%m/%Y").replace(hour=23, minute=59, second=59)

        #lists the URLs of the news until the stop date given
        news_to_scrap = list_news_until_date(stop_date)

        counter = 0

        scrapedNews = []

        #loop where each new is scrapped
        for news in news_to_scrap:
            counter = counter + 1
            scraped = scrap(news)
            scrapedNews.append(scraped)
            print(scraped)
            print("Scraped: %d / %d" % (counter, len(news_to_scrap)))

        df = pd.DataFrame.from_dict(scrapedNews, orient='columns')
        df.to_csv(path_or_buf=path, sep=';', index=False, encoding="utf-8")
    else:
        None
    
    #if argument show graphs provided
    if args.show_graphs is True:

        if os.path.isfile(path):
            graphics_object = MeneameGraphicsManager(path)
            graphics_object.show()
        else:
            raise Exception("Output CSV not found. Add option --stop_date to create it")


