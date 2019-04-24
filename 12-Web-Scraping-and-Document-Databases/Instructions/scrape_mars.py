from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests 


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser('chrome', **executable_path, headless=False)


mars_info = {}

def scrape():
    try:
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = bs(html, 'html.parser')

        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text
        mars_info['news_title']= news_title
        mars_info['news_p']= news_p

        return mars_info
    finally:
        browser.quit()

#FEATURED IMAGE
def image():
    
    try:
        browser = init_browser()
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)

        html = browser.html
        soup = bs(html, 'html.parser')

        image = soup.find("img", class_="thumb")["src"]
        featured_image_url = "https://www.jpl.nasa.gov" + image
        mars_info['featured_image_url'] = featured_image_url

        return mars_info
    finally:
        browser.quit()

#MARS WEATHER
def weather():
    
    try:
        browser = init_browser()
        twitter_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(twitter_url)

        html = browser.html
        soup = bs(html, 'html.parser')

        tweets = soup.find_all("div",class_="js-tweet-text-container")
        
        for tweet in tweets:
            mars_weather = tweet.p.text
            mars_info['mars_weather'] = mars_weather
        return mars_info
    finally:
        browser.quit()

#MARS FACTS
def facts():
   
    try:
        browser = init_browser()
        facts_url = "https://space-facts.com/mars/"
        tables = pd.read_html(facts_url)

        df = tables[0]
        df.columns = ['Name','Value']
        mars_info['facts']= df.to_html(classes="table table-sm", header=False, index=False)

        return mars_info
    finally:
        browser.quit()

def hemisphere():

    try:
        browser = init_browser()
        hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hem_url)

        html = browser.html 
        soup = bs(html,"html.parser")
        items = soup.find_all("div", class_='item')

        hemisphere_image_urls = []
        main_url = "https://astrogeology.usgs.gov"
        for item in items: 
            title = item.find('h3').text
            item_url = item.find('a', class_='itemLink product-item')['href']
            browser.visit(main_url + item_url)
            item_html = browser.html 
            soup = bs(item_html, 'html.parser')
            img_url = soup.find('div', class_='downloads').find("a")["href"]

            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        return mars_info
    finally:
        browser.quit()
        
        
