import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import csv
import time

def main():
    writer, file = files()
    soup = set_page()
    scrape(soup, writer)
    file.close()


def collect_apartments(apartments, soup):
    # function to retrieve pages
    layer = soup.find_all('a')
    links = []
    for i in layer:
        links.append(i['href'])
    link = [i for i in links if ('https://www.domain.com.au/' in i)]
    rents = []
    for a in link:
        if a in rents:
            continue
        else:
            rents.append(a)

    pattern = 'https://www.domain.com.au/[\w?\d+\w?\-]+[\D+\-]+\d{4}\-\d{8}[\?topspot=1]?'
    for n in rents:
        if re.findall(pattern, n):
            apartments.append(n)
    # function to retrieve pages

def data_scrape(apartments, index, writer):
    # function for data collecting
    if(index % 20 == 0):
        time.sleep(5)

    # retrieve html
    unit = apartments.pop(0)
    page = requests.get(unit)
    soup_in = BeautifulSoup(page.text, 'html.parser')
    # retrieve html
    
    # scrape geographic location
    addr = soup_in.find_all('h1', class_ = 'css-164r41r')
    try:
        address = addr[0].text
        pattern = '\w?\d+\w?\/\w?\d+\w?\-?\d*\s+[\w+\s]+'
        street = re.findall(pattern, address)
        name = street[0].split()
        indexing = len(name[-1]) + len(name[-2]) + len(name[-3]) + 3
        street_only = street[0][:-indexing]
        subs = name[-3]
        code = name[-1]
        state = name[-2]
    except:
        street_only = np.nan
        subs = np.nan
        code = np.nan
        state = np.nan
    # scrape geographic location
    
    # scrape prices
    price = soup_in.find_all('div', class_ = 'css-1texeil')
    try:
        rent_desc = price[0].text
        rent_num = int(re.findall('\d+', rent_desc)[0])
    except:
        rent_num = np.nan
        
    try:    
        uls = soup_in.find_all('ul', class_ = 'css-1h9anz9')[0]
        strongs = uls.find_all('strong')
        for i in strongs:
            re.findall('\$\d+', i.text)
            if (re.findall('\$\d+', i.text)):
                bond = int(re.findall('\$\d+', str(i))[0][1:])
            else:
                bond = np.nan
    except:
        bond = np.nan
    # scrape prices
            
    # scrape property agent
    agents = soup_in.find_all('p', class_ = 'listing-details__agent-enquiry-agent-company-name')
    try:
        agent = agents[0].text
    except:
        agent = np.nan
    # scrape property agent
    
    # scrape property features
    try:
        features = soup_in.find_all('div', class_='css-18biwo')
        num_features = features[0].text
        beds = int(re.findall('\d Bed', num_features)[0][0])
        baths = int(re.findall('\d Bath', num_features)[0][0])
    except:
        beds = np.nan
        baths = np.nan
    try:
        parks = int(re.findall('[\d] Parking', num_features)[0][0])
    except:
        parks = int(0)
        
    html = soup_in.find_all('div', class_ = 'noscript-expander-wrapper css-aeox7o')
    heating = 0
    aircon = 0
    balcony = 0
    dishwasher = 0
    gym = 0
    for markups in html:
        if re.findall("heating|heater", str(markups.text).lower()):
            heating = 1
        if re.findall("air conditioning|air conditioner| ac | air con |cooling", str(markups.text).lower()):
            aircon = 1
        if re.findall("balcony\balconies", str(markups.text).lower()):
            balcony = 1
        if re.findall("dishwasher", str(markups.text).lower()):
            dishwasher = 1
        if re.findall("gym", str(markups.text).lower()):
            gym = 1
    # scrape property features
    
    # scrape neighbourhood information   
    schools = soup_in.find_all('div', class_ = 'css-si4svp')
    dis = []
    try:
        for div in schools:
            text = float(div.text[:3])
            dis.append(text)
            break
        gov_school = float(dis[0])
    except:
        gov_school = np.nan
    
    try:
        schools = soup_in.find_all('table', class_ = 'css-8atqhb')[0].tbody
        demo = schools.find_all('div', class_ = 'css-199ul8s')
        demographics = ['Under 20', '20-39', '40-59', '60+']
        percentage = []
        for age in demo:
            percentage.append(int(age.text[:-1]))
        max_index = percentage.index(max(percentage))
        largest_demo = demographics[max_index]
    except:
        largest_demo = np.nan
    # scrape neighbourhood information   
    
    print((str(index+1)+"."), street_only, subs, code, state)
    time.sleep(3)
    if (street_only != np.nan):
        writer.writerow([street_only, subs, code, state, rent_num, bond, agent, 
        beds, baths, parks, heating, aircon, balcony, dishwasher, gym, gov_school, 
        largest_demo])
    # function for data collecting
    return True

def files():
    # open csv file
    FILENAME = 'Apartments2.csv'
    file = open(FILENAME ,'w+')
    writer = csv.writer(file)
    writer.writerow(['Address', 'Suburb', 'Code', 'State', 'Rent', 'Bond', 
                                 'Agent','Bedroom', 'Bathroom', 'Parking', 'Heating',
                                 'Air Conditioning', 'Balcony', 'Dishwasher', 
                                 'Gym', 'Distance (km) to closest public school',
                                 'Neighbourhood Largest Demographics'])
    return writer, file
    # open csv file

def set_page():
    # url set up
    url = 'https://www.domain.com.au/rent/melbourne-region-vic/apartment/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
    # url set up
 
def scrape(soup, writer):
    # Scraper function
    base_url = 'https://www.domain.com.au'
    # scraping page 1
    index = 0
    pages = []
    apartments = []
    collect_apartments(apartments, soup)
    
    while(apartments):
        data_scrape(apartments, index, writer)
        index += 1
    
    next_page = soup.find('a', class_ = 'css-17ze22x')['href']
    next_url = base_url + next_page
    pages.append(next_url)
    # scraping page 1
    
    # web scraping
    
    while(pages):
        # parse current page
        url = pages.pop(0)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # parse current page
        
        # retrieve next page
        try:
            next_page = soup.find('a', class_ = 'css-17ze22x')['href']
            next_url = base_url + next_page
            pages.append(next_url)
        except TypeError:
            continue
        # retrieve next page
    
        # retrieve links for current page 
        collect_apartments(apartments)
        # retrieve links for current page 
        
        # collect data in subjects page
        while(apartments):
            if index == 10:
                break
            data_scrape(apartments, index, writer)
            index += 1
        # collect data in subjects page
    # Scraper function
    
main()




