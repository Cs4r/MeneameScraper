#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import argparse

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


def epoch_to_formatted_date(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))


def string_to_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def scrap(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="html.parser")
    news = dict()

    news["title"] = soup.title.text

    news["paragraph"] = soup.find(class_="news-content").text

    tags = []
    for link in soup.select(".news-tags a"):
        tags.append(link.text.strip())
    news["tags"] = tags

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
    page_number = 1
    list_of_urls = []
    fetch_news = True

    while fetch_news:
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


def write_header(file, news, separator):
    keys = list(news[0].keys())
    headers = separator.join(keys) + "\n"
    file.write(headers)
    return keys


def write_line(file, news, columns, separator):
    line = ""
    for c in columns:
        if type(news[c]) == list:
            line = line + ",".join(news[c]) + separator
        elif type(news[c]) == int:
            line = line + str(news[c]) + separator
        elif type(news[c]) == str:
            line = line + news[c].replace(separator, "") + separator

    line = line[:-1]
    file.write(line)
    file.write("\n")
    file.flush()


def data_to_csv(filename, news=None):
    with open("./csv/" + filename, "w+") as file:
        if news:
            separator = ";"
            keys = write_header(file, news, separator)
            for n in news:
                write_line(file, n, keys, separator)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--stop_date", help="date to stop fetching news")
    args = parser.parse_args()

    stop_date = datetime.strptime(args.stop_date, "%d/%m/%Y").replace(hour=23, minute=59, second=59)

    news_to_scrap = list_news_until_date(stop_date)

    counter = 0

    scrapedNews = []

    for news in news_to_scrap:
        counter = counter + 1
        scraped = scrap(news)
        scrapedNews.append(scraped)
        print(scraped)
        print("Scraped: %d / %d" % (counter, len(news_to_scrap)))
        # time.sleep(1.5)

    data_to_csv("dataset.csv", scrapedNews)
