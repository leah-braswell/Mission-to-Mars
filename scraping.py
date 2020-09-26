#import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas
import pandas as pd

#set the executable path and ititialize the chrom browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

#visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Optional delay for loading the page
#search for ul and li tags and wait one second before searching components
browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

#inside the slide variable look for the div tag and find the content title
slide_elem.find('div', class_='content_title')

#use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#inside the slide variable look for the div tag and find the article summary
slide_elem.find('div', class_='article_teaser_body')

#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ## Featured Images

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

#find the relative image url (follow the nested tags in the order given)
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

#use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ## Mars Facts

#create a pandas dataframe from the HTML table [0] means pull only the first table found
df = pd.read_html('http://space-facts.com/mars/')[0]
#assign columns to the new dataframe for additional clarity
df.columns=['description', 'value']
#turn the description column into the dataframe's index
df.set_index('description', inplace=True)
#call the dataframe
df

#convert dataframe back to HTML
df.to_html()

#end the automated browsing session
browser.quit()




