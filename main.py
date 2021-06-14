import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import pandas as pd
import random

PATH = r'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(executable_path=PATH)

url = "https://www.immowelt.at/liste/wien-3-landstrasse/wohnungen/kaufen?prima=350000&wflmi=50&bjma=1960&sort=createdate%2Bdesc"
# up to 350000€
# built 1960 or earlier
# 50 square meters or more

driver.get(url)
time.sleep(random.randrange(4, 6)*1.15)


# Handling Cookies
# Cookies are processed via the Consent Management Platform usercentrics
element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector('section div div div div div div div button[data-testid="uc-customize-button"]')""")
element.click()
time.sleep(random.randrange(5, 7)*1.25)
element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector('section div div div div div div div button[data-testid="uc-deny-all-button"]')""")
element.click()
time.sleep(random.randrange(3, 5)*1.15)


# Dealing with AJAX elements
# The website loads part of the content when scrolling down
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scrolls to bottom of page
time.sleep(random.randrange(3, 6)*1.05)


# Parsing the document
pageSource = driver.page_source
driver.close()

bsObj = BeautifulSoup(pageSource, "html.parser")

list_links = []
tagObj_href = bsObj.find_all("a", href=re.compile("expose"))
for i in tagObj_href:
    j = i["href"]
    list_links.append(j)

print(list_links)


# Setting up lists that form the dataframe
link_expose = [] # works as ID
price = []
#listingTime = []
squaremeters = []
#floor = []
#thumbnails = []
#description = []
rooms = []
#buildYear = []


# Getting links to all listing pages
for i in list_links:
    link_expose.append("https://www.immowelt.at" + i)
print(link_expose)


# Getting the data from each listing
for i in link_expose:
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(i)
    time.sleep(random.randrange(4, 7)*1.25)

    element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector('section div div div div div div div button[data-testid="uc-customize-button"]')""")
    element.click()
    time.sleep(random.randrange(3, 6)*1.05)
    element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector('section div div div div div div div button[data-testid="uc-deny-all-button"]')""")
    element.click()
    time.sleep(random.randrange(3, 5)*1.25)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scrolls to bottom of page
    time.sleep(random.randrange(4, 7)*1.15)

    pageSource_expose = driver.page_source
    print("Source document successfully retrieved")
    driver.close()

    bsObj_expose = BeautifulSoup(pageSource_expose, "html.parser")
    tagObj_price, tagObj_squaremeters, tagObj_rooms = bsObj_expose.find_all(class_="hardfact", limit=3)

    # Price
    price_item = tagObj_price.text
    price_item = re.sub("\D", " ", price_item) # substitutes non-digit characters
    price_item = price_item.strip()
    price_item = x = re.sub(" ", "", price_item)
    price.append(price_item)

    # Squaremeters
    squaremeters_item = tagObj_squaremeters.text
    squaremeters_item = re.sub("\D", " ", squaremeters_item) # substitutes non-digit characters
    squaremeters_item = squaremeters_item.strip()
    squaremeters_item = re.sub(" ", ".", squaremeters_item)
    squaremeters.append(squaremeters_item)

    # Rooms
    rooms_item = tagObj_rooms.text
    rooms_item = re.sub("\D", " ", rooms_item) # substitutes non-digit characters
    rooms_item = rooms_item.strip()
    rooms.append(rooms_item)


# Creating the dataframe and writing to a csv file
cols = ['Price', 'Squaremeters', 'Rooms']
df = pd.DataFrame({'Price':price,
                   'Squaremeters':squaremeters,
                   'Rooms':rooms})[cols]
df.to_csv('Vienna_raw.csv')