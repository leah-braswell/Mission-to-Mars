#!/usr/bin/env python
# coding: utf-8

# In[126]:


#import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas
import pandas as pd


# In[127]:


#set the executable path and ititialize the chrom browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


#visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Optional delay for loading the page
#search for ul and li tags and wait one second before searching components
browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)


# In[4]:


#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')



#inside the slide variable look for the div tag and find the content title
slide_elem.find('div', class_='content_title')



#use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

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


# ### Mars Facts

#create a pandas dataframe from the HTML table [0] means pull only the first table found
df = pd.read_html('http://space-facts.com/mars/')[0]
#assign columns to the new dataframe for additional clarity
df.columns=['Description', 'Mars']
#turn the description column into the dataframe's index
df.set_index('Description', inplace=True)
#call the dataframe
df

df.to_html()


# ### Mars Weather

# In[15]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[16]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[17]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 

# ### Hemispheres

# In[167]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[189]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
images = browser.find_by_css('h3')


# In[190]:


x = 0
for image in images:
    image = browser.find_by_css('h3')[x]
    image.click()
    html = browser.html
    hem_image = soup(html, 'html.parser')
    hem_img = hem_image.select_one('div.downloads ul li a').get('href')
    title = hem_image.find('h2').get_text()
    hemisphere_image_urls.append({"image": hem_img, "title": title})
    x = x+1
    browser.back()
    continue
   




# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


#end the automated browsing session
browser.quit()


# In[ ]:




