from bs4 import BeautifulSoup
import re
import requests

url = "https://www.immowelt.at/liste/wien-3-landstrasse/wohnungen/kaufen?prima=350000&wflmi=50&bjma=1945&sort=createdate%2Bdesc"
# up to 350000€
# built 1945 or earlier
# 50 square meters or more

page = requests.get(url)
html_doc = page.content
#print(html_doc)

bsObj = BeautifulSoup(html_doc, "html.parser")
print(bsObj.prettify())

# setting up lists that form the dataframe
price = []
listingTime = []
squaremeters = []
floor = []
thumbnails = []
url = []
description = []

tagObj_squaremeters = bsObj.find_all(class_="hardfact square_meters")
print(tagObj_squaremeters)

for i in tagObj_squaremeters:
    x = i.text
    x = str(x)
    x = re.sub("\D", " ", x) # substitutes non-digit characters
    x = x.strip()
    x = re.sub(" ", ".", x)
    x = float(x)
    squaremeters.append(x)

print(squaremeters)


#tagObj_price = bsObj.find_all(class_="hardfact price_sale")
#print(tagObj_price)
