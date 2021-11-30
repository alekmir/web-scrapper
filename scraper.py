from string import punctuation
from requests import get
from bs4 import BeautifulSoup
from os import mkdir


def punctuation_killer(text):
    for symbol in text:
        if symbol == " ":
            text = text.replace(" ", "_")
        elif symbol in punctuation:
            text = text.replace(symbol, "")
    return text


def list_creator(type, link):
    soup = BeautifulSoup(get(link, headers={'Accept-Language': 'en-US,en;q=0.5'}).content, 'html.parser')
    articles = soup.find_all("article")
    links = []
    link_begins_with = "https://www.nature.com"
    for article in articles:
        spans = article.find_all('span', {'class': "c-meta__type"})
        for span in spans:
            if span.contents[0] == type:
                a = article.find_all("a")
                for href in a:
                    links.append(link_begins_with + href.get("href"))
    return links


def grabber(link, folder, article_type):
    soup = BeautifulSoup(get(link, headers={'Accept-Language': 'en-US,en;q=0.5'}).content, 'html.parser')
    title = punctuation_killer(soup.title.contents[0])
    file = open(f"{folder}\{title}.txt", "w", encoding="utf-8")
    data_text = "No data!"
    if article_type == "Article":
        data_text = article(soup)
    elif article_type == "Author Correction":
        data_text = article(soup)
    elif article_type == "Book Review":
        data_text = main(soup)
    elif article_type == "Career Column":
        data_text = main(soup)
    elif article_type == "Comment":
        data_text = main(soup)
    elif article_type == "Correspondence":
        data_text = main(soup)
    elif article_type == "Editorial":
        data_text = main(soup)
    elif article_type == "Futures":
        data_text = main(soup)
    elif article_type == "Nature Briefing":
        data_text = main(soup)
    elif article_type == "Nature Index":
        data_text = nature_index(soup)
    elif article_type == "Nature Podcast":
        data_text = nature_podcast(soup)
    elif article_type == "News":
        data_text = main(soup)
    elif article_type == "News & Views":
        data_text = news_views(soup)
    elif article_type == "News Feature":
        data_text = main(soup)
    elif article_type == "News Round-Up":
        data_text = main(soup)
    elif article_type == "Outlook":
        data_text = main(soup)
    elif article_type == "Publisher Correction":
        data_text = nature_index(soup)
    elif article_type == "Research Highlight":
        data_text = news_views(soup)
    elif article_type == "Where I Work":
        data_text = main(soup)
    elif article_type == "World View":
        data_text = main(soup)
    else:
        print("Error: Unknown article type in user demand!")
    file.write(data_text)
    file.close()
    print(f"Writing complete: {title}.txt")


def article(soup):
    div = soup.find("div", {"class": "c-article-body"})
    return div.text.strip()


def nature_index(soup):
    div = soup.find("div", {"class": "c-article-body"})
    return div.text.strip()


def nature_podcast(soup):
    article = str()
    # Gathering announce text which usually placed under the article image
    div = soup.find("div", {"class": "c-article-body u-clearfix"})
    h3 = div.find("h3")
    article = article + h3.text
    # Gathering article text
    p = div.find_all("p")
    for i in range(1, len(p)):
        article = article + p[i].text
    return article.strip()


def main(soup):
    div = soup.find("div", {"class": "c-article-body u-clearfix"})
    return div.text.strip()


def news_views(soup):
    div = soup.find("main", {"class": "c-article-main-column u-float-left"})
    return div.text.strip()


pages_count = int(input()) + 1
article_type = input()
for i in range(1, pages_count):
    try:
        mkdir(f"Page_{i}")
    except FileExistsError:
        pass
    links = list_creator(
        article_type,
        f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i}")
    for link in links:
        grabber(link, f"Page_{i}", article_type)
