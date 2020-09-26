#import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas
import pandas as pd
#import datetime
import datetime as dt

#define scraping function
def scrape_all():
    #set the executable path and ititialize the chrom browser in splinter
    browser = Browser('chrome', executable_path = 'chromedriver', headless=True)

    news_title, news_paragraph = mars_news(browser)

    #rund all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    #stop webdriver and return data
    browser.quit()
    return data     

#define mars_news scraping function
def mars_news(browser):

    #visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    #Optional delay for loading the page
    #search for ul and li tags and wait one second before searching components
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        #inside the slide variable look for the div tag and find the content title
        #slide_elem.find('div', class_='content_title')

        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        #inside the slide variable look for the div tag and find the article summary
        #slide_elem.find('div', class_='article_teaser_body')

        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    #return statement
    return news_title, news_p

# ## Featured Images
def featured_image(browser):

    #visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    #use text to find elements
    #allow 1 second to load and return Boolean if the element is present or not
    browser.is_element_present_by_text('more info', wait_time=1)
    #create new variable and ask splinter to search for the string of text
    more_info_elem = browser.links.find_by_partial_text('more info')
    #click on the element
    more_info_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #try/except for error handling
    try:
        #find the relative image url (follow the nested tags in the order given)
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    #use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():

    try:
        #create a pandas dataframe from the HTML table [0] means pull only the first table found
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    #assign columns to the new dataframe for additional clarity
    df.columns=['description', 'value']
    #turn the description column into the dataframe's index
    df.set_index('description', inplace=True)
    #convert dataframe back to HTML
    return df.to_html(classes='table table-striped')

   
if __name__ =='__main__':
    print(scrape_all())


