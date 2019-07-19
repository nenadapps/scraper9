from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass

    return html_content

def get_countries(url):
    items = []
    try:
        html = get_html(url)
        country_items = html.select('.menuleft a')
        for country_item in country_items:
            country_href = country_item.get('href')
            if "cat_id" in country_href: 
                item = 'http://www.philatelic-items.co.uk/' + country_href
                items.append(item)
    except: 
        pass

    return items

def get_page_items(url):

    items = []
    country_name = ''

    try:
        html = get_html(url)
    except:
        return items

    try:
        country_name_temp = html.select(".header")[0].get_text()
        country_name_parts = country_name_temp.split("-")
        country_name = country_name_parts[0].strip()
    except:
        pass

    try:
        for item in html.select('td b a'):
            item = 'http://www.philatelic-items.co.uk' + item.get('href')
            items.append(item)
    except: 
        pass

    shuffle(items)

    return items, country_name

def get_details(url, country_name):

    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        td_items = html.select('table table td p strong')
        for td_item in td_items:
            heading = td_item.get_text().strip()
            value = td_item.parent.get_text().strip()
            value = value.replace(heading, '').strip()
            if(heading == 'Price:'):
                price = value.replace('£', '').strip()
                stamp['price'] = price
            elif(heading == 'Date of issue:'):
                date_of_issue = value
                stamp['date_of_issue'] = date_of_issue
            elif(heading == 'Face Value/Country:'):
                raw_text = value
                stamp['raw_text'] = raw_text
            elif(heading == 'SG:'):
                sg = value
                stamp['sg'] = sg
            elif(heading == 'Condition:'):
                condition = value
                stamp['condition'] = condition    
    except:
        stamp['price'] = None
        stamp['date_of_issue'] = None
        stamp['raw_text'] = None
        stamp['sg'] = None
        stamp['condition'] = None

    stamp['country'] = country_name
    stamp['currency'] = 'GBP'

    # image_urls should be a list
    images = []
    try:
        image_items = html.find_all("td", {"align":"center"})
        for image_item in image_items:
            img_src = image_item.find('img').get('src')
            img = 'http://www.philatelic-items.co.uk/' + img_src
            images.append(img)
    except:
        pass

    stamp['image_urls'] = images 
    
    stamp['url'] = url

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    print(stamp)
    print('+++++++++++++')
    sleep(randint(22, 99))

    return stamp

# start url
start_url = 'http://www.philatelic-items.co.uk/'

# loop through all countries
countries = get_countries(start_url)
for country in countries:
    flag = True
    start_page = 0
    while(flag):
        page_url = country + '&start_page=' + str(start_page)
        page_items, country_name = get_page_items(page_url)
        # loop through all items on current page
        if page_items:
            for page_item in page_items:
                stamp = get_details(page_item, country_name) 
        else:
            flag = False  
        start_page = start_page + 20      